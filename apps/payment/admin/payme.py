from django.contrib import admin
from payme.models import Order, MerchantTransactionsModel
from unfold.admin import ModelAdmin

admin.site.unregister(Order)
admin.site.unregister(MerchantTransactionsModel)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "amount",
        "created_at",
    )


@admin.register(MerchantTransactionsModel)
class MerchatTransactionsModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "transaction_id",
        "order_id",
        "amount",
        "reason",
    )
