import os

PAYME: dict = {
    'PAYME_ID': os.getenv('PAYME_ID'),
    'PAYME_KEY': os.getenv('PAYME_KEY'),
    'PAYME_URL': os.getenv('PAYME_URL'),
    'PAYME_CALL_BACK_URL': os.getenv('PAYME_CALL_BACK_URL'),
    'PAYME_MIN_AMOUNT': os.getenv('PAYME_MIN_AMOUNT'),
    'PAYME_ACCOUNT': os.getenv('PAYME_ACCOUNT'),
}

ORDER_MODEL = 'apps.ticket.Order'
