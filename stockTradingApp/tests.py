from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, StockData, Transaction

# test case for user resgistraion


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            'username': 'testuser',
            'balance': 1000.00
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


# test case for user data
class UserRetrievalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='existinguser', balance=2000.00)

    def test_user_retrieval(self):
        url = reverse('user-data', args=['existinguser'])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')

# test case for stock addition
class StockIngestionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_stock_ingestion(self):
        url = reverse('stock-ingest')
        data = {
            'ticker': 'AAPL',
            'open_price': 150.00,
            'close_price': 155.00,
            'high': 160.00,
            'low': 145.00,
            'volume': 100000,
            'timestamp': '2022-01-01T12:00:00Z'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockData.objects.count(), 1)
        self.assertEqual(StockData.objects.get().ticker, 'AAPL')

# test case for stock fetching
class StockDataRetrievalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        StockData.objects.create(
            ticker='AAPL',
            open_price=150.00,
            close_price=155.00,
            high=160.00,
            low=145.00,
            volume=100000,
            timestamp='2022-01-01T12:00:00Z'
        )

    def test_stock_data_list(self):
        url = reverse('stock-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_stock_data_detail(self):
        url = reverse('stock-detail', args=['AAPL'])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticker'], 'AAPL')


#test case for transaction
class TransactionCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', balance=2000.00)
        StockData.objects.create(
            ticker='AAPL',
            open_price=150.00,
            close_price=155.00,
            high=160.00,
            low=145.00,
            volume=100000,
            timestamp='2022-01-01T12:00:00Z'
        )

    def test_transaction_creation_buy(self):
        url = reverse('transaction-create')
        data = {
            'user_id': self.user.pk,
            'ticker': 'AAPL',
            'transaction_type': 'buy',
            'transaction_volume': 10
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().transaction_type, 'buy')
        self.assertEqual(User.objects.get(id=self.user.pk).balance, 2000.00 - (10 * 155.00))  # Assuming close_price as transaction price

    def test_transaction_creation_sell(self):
        url = reverse('transaction-create')
        data = {
            'user_id': self.user.pk,
            'ticker': 'AAPL',
            'transaction_type': 'sell',
            'transaction_volume': 5
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().transaction_type, 'sell')
        self.assertEqual(User.objects.get(id=self.user.pk).balance, 2000.00 + (5 * 155.00))