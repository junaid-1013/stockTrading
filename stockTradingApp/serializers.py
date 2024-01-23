from rest_framework import serializers
from .models import User, StockData, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'balance']


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['ticker', 'open_price', 'close_price',
                  'high', 'low', 'volume', 'timestamp']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'user', 'ticker', 'transaction_type',
                  'transaction_volume', 'transaction_price', 'timestamp']
