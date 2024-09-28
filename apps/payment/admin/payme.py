from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = (
        "id",
        "amount",
        "status",
        "type",
        "created_at",
        "order_id",
    )
    list_filter = ("status", "type")
    search_fields = ("order_id", "transaction_id")
