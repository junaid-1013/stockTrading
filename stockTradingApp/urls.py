from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserRegistration.as_view(), name='user-registration'),
    path('users/<str:username>/', views.UserData.as_view(), name='user-data'),
    path('stocks/', views.StockDataIngest.as_view(), name='stock-ingest'),
    path('stocks/list/', views.StockDataList.as_view(), name='stock-list'),
    path('stocks/<str:ticker>/',
         views.StockDataDetail.as_view(), name='stock-detail'),
    path('transactions/', views.TransactionCreate.as_view(),
         name='transaction-create'),
    path('transactions/<int:user_id>/',
         views.UserTransactions.as_view(), name='user-transactions'),
    path('transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/',
         views.UserTransactionsByTimestamp.as_view(), name='user-transactions-timestamp'),
]
