from django.db import DatabaseError

from apps.payme.utils.logging import logger
from apps.payme.models import MerchantTransactionsModel
from apps.payme.serializers import MerchantTransactionsModelSerializer as MTMS


class CheckTransaction:
    """
    CheckTransaction class
    That's used to check transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checkperformtransaction
    """

    def __call__(self, params: dict) -> tuple:
        clean_data: dict = MTMS.get_validated_data(params=params)

        try:
            transaction = MerchantTransactionsModel.objects.get(
                _id=clean_data.get("_id"),
            )
            response = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "perform_time": transaction.perform_time,
                    "cancel_time": transaction.cancel_time,
                    "transaction": transaction.transaction_id,
                    "state": transaction.state,
                    "reason": None,
                }
            }
            if transaction.reason is not None:
                response["result"]["reason"] = int(transaction.reason)

        except DatabaseError as error:
            logger.error("Error getting transaction in database: %s", error)

        return None, response
