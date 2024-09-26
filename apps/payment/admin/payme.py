from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = (
        "id",
        "amount",
        "created_at",
    )
