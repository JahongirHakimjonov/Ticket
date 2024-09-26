import os

PAYME: dict = {
    'PAYME_ID': str(os.getenv('PAYME_ID')),
    'PAYME_KEY': str(os.getenv('PAYME_KEY')),
    'PAYME_URL': str(os.getenv('PAYME_URL')),
    'PAYME_CALL_BACK_URL': str(os.getenv('PAYME_CALL_BACK_URL')),
    'PAYME_MIN_AMOUNT': int(os.getenv('PAYME_MIN_AMOUNT')),
    'PAYME_ACCOUNT': str(os.getenv('PAYME_ACCOUNT')),
}

ORDER_MODEL = 'apps.ticket.Order'
