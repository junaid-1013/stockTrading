from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, StockData, Transaction
from .serializers import UserSerializer, StockDataSerializer, TransactionSerializer
from .tasks import process_transaction
from django.core.cache import cache

# POST /users/: To register a new user with a username and initial balance.
class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /users/{username}/: To retrieve user data.
class UserData(APIView):
    def get(self, request, username, *args, **kwargs):
        user_cache_key = f"user_{username}"
        user_data = cache.get(user_cache_key)

        if not user_data:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            user_data = serializer.data
            cache.set(user_cache_key, user_data)

        return Response(serializer.data)


# POST /stocks/: To ingest stock data and store it in the Postgres database.
class StockDataIngest(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /stocks/: To retrieve all stock data.
class StockDataList(APIView):
    def get(self, request, *args, **kwargs):
        stock_cache_key = "stock_list"
        stock_data = cache.get(stock_cache_key)

        if not stock_data:
            stocks = StockData.objects.all()
            serializer = StockDataSerializer(stocks, many=True)
            stock_data = serializer.data
            cache.set(stock_cache_key, stock_data)

        return Response(serializer.data)


# GET /stocks/{ticker}/: To retrieve specific stock data.
class StockDataDetail(APIView):
    def get(self, request, ticker, *args, **kwargs):
        stock_cache_key = f"stock_{ticker}"
        stock_data = cache.get(stock_cache_key)

        if not stock_data:
            try:
                stock = StockData.objects.get(ticker=ticker)
            except StockData.DoesNotExist:
                return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = StockDataSerializer(stock)
            stock_data = serializer.data
            cache.set(stock_cache_key, stock_data)
            
        return Response(serializer.data)

# POST /transactions/: To post a new transaction.


class TransactionCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            process_transaction.delay(transaction.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /transactions/{user_id}/: To retrieve all transactions of a specific user.


class UserTransactions(APIView):
    def get(self, request, user_id, *args, **kwargs):
        transactions = Transaction.objects.filter(user_id=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


# GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/: To retrieve transactions of a specific user between two timestamps.
class UserTransactionsByTimestamp(APIView):
    def get(self, request, user_id, start_timestamp, end_timestamp, *args, **kwargs):
        transactions = Transaction.objects.filter(
            user_id=user_id, timestamp__range=(start_timestamp, end_timestamp)
        )
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
