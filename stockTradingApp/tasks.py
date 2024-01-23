from celery import shared_task
from .models import Transaction


@shared_task
def process_transaction(transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        # Perform transaction processing logic here
        # For example, update user balance based on transaction details
        # ...
        transaction.processed = True
        transaction.save()
    except Transaction.DoesNotExist:
        pass