from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.payme.models import CUSTOM_ORDER
from apps.payme.models import Order as DefaultOrderModel

from apps.payme.models import MerchantTransactionsModel

if not CUSTOM_ORDER:
    admin.site.register(DefaultOrderModel)


@admin.register(MerchantTransactionsModel)
class MerchantTransactionsModelAdmin(ModelAdmin):
    list_display = (
        "_id",
        "order_id",
        "transaction_id",
        "amount",
        "state",
        "created_at",
    )
    search_fields = ("order_id", "transaction_id")
    list_filter = ("state",)
