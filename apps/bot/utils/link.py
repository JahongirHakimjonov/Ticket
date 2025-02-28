import base64
import os
from dataclasses import dataclass
from decimal import Decimal

PAYME_ID = os.getenv("PAYME_ID")
PAYME_ACCOUNT = os.getenv("PAYME_ACCOUNT")
PAYME_CALL_BACK_URL = os.getenv("PAYME_CALL_BACK_URL")
PAYME_URL = os.getenv("PAYME_URL")


@dataclass
class GeneratePayLink:
    """
    GeneratePayLink dataclass
    That's used to generate pay lint for each order.

    Parameters
    ----------
    order_id: int — The order_id for paying
    amount: int — The amount belong to the order
    callback_url: str \
        The merchant api callback url to redirect after payment. Optional parameter.
        By default, it takes PAYME_CALL_BACK_URL from your settings

    Returns str — pay link
    ----------------------

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/initsializatsiya-platezhey/
    """

    order_id: str
    amount: Decimal
    callback_url: str = None

    def generate_link(self) -> str:
        """
        GeneratePayLink for each order.
        """
        generated_pay_link: str = "{payme_url}/{encode_params}"
        params: str = (
            "m={payme_id};ac.{payme_account}={order_id};a={amount};c={call_back_url}"
        )

        if self.callback_url:
            redirect_url = self.callback_url
        else:
            redirect_url = PAYME_CALL_BACK_URL

        params = params.format(
            payme_id=PAYME_ID,
            payme_account=PAYME_ACCOUNT,
            order_id=self.order_id,
            amount=self.amount,
            call_back_url=redirect_url,
        )
        encode_params = base64.b64encode(params.encode("utf-8"))
        return generated_pay_link.format(
            payme_url=PAYME_URL, encode_params=str(encode_params, "utf-8")
        )

    @staticmethod
    def to_tiyin(amount: Decimal) -> Decimal:
        """
        Convert from sum to tiyin.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount * 100

    @staticmethod
    def to_sum(amount: Decimal) -> Decimal:
        """
        Convert from tiyin to sum.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount / 100
