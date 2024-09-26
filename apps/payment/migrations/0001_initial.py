# Generated by Django 5.0.8 on 2024-09-26 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ticket", "0010_concert_address_ru_concert_address_uz_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PROCESSING", "Processing"),
                            ("COMPLETED", "Completed"),
                            ("FAILED", "Failed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PROCESSING",
                        max_length=100,
                    ),
                ),
                ("transaction_id", models.CharField(max_length=255)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CLICK", "Click"),
                            ("PAYME", "Payme"),
                            ("OCTO", "OCTO"),
                            ("CASH", "Cash"),
                        ],
                        default="PAYME",
                        max_length=100,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("message", models.TextField(blank=True, null=True)),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ticket.order"
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
                "db_table": "payment",
            },
        ),
    ]
