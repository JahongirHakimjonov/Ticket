# Generated by Django 5.0.8 on 2024-09-24 06:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0003_rename_start_date_concert_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="concert_seats",
        ),
        migrations.RemoveField(
            model_name="concert",
            name="hall",
        ),
        migrations.RemoveField(
            model_name="seat",
            name="hall",
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "Buyurtma", "verbose_name_plural": "Buyurtmalar"},
        ),
        migrations.RemoveField(
            model_name="seat",
            name="row",
        ),
        migrations.RemoveField(
            model_name="seat",
            name="seat_number",
        ),
        migrations.AddField(
            model_name="concert",
            name="address",
            field=models.CharField(
                default=django.utils.timezone.now, max_length=255, verbose_name="Manzil"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="concert",
            name="location_google_maps",
            field=models.URLField(
                default=django.utils.timezone.now,
                max_length=255,
                verbose_name="Google Maps manzili",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="concert",
            name="location_yandex_maps",
            field=models.URLField(
                default=django.utils.timezone.now,
                max_length=255,
                verbose_name="Yandex Maps manzili",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="count",
            field=models.PositiveIntegerField(default=0, verbose_name="Soni"),
        ),
        migrations.AddField(
            model_name="order",
            name="seat",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="ticket.seat",
                verbose_name="Joy",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="seat",
            name="concert",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="ticket.concert",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="seat",
            name="count",
            field=models.PositiveIntegerField(default=1, verbose_name="Joylar soni"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="seat",
            name="name",
            field=models.CharField(default=1, max_length=255, verbose_name="Nomi"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="concert",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="concerts/thumbnail",
                verbose_name="Mini rasm",
            ),
        ),
        migrations.AlterField(
            model_name="donate",
            name="message",
            field=models.TextField(blank=True, null=True, verbose_name="Xabar"),
        ),
        migrations.AlterField(
            model_name="donate",
            name="phone",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Telefon raqam"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="concert",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ticket.concert",
                verbose_name="Konsert",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Yaratilgan sana"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=100, verbose_name="Jami narx"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ticket.botusers",
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AlterModelTable(
            name="order",
            table="order",
        ),
        migrations.DeleteModel(
            name="ConcertSeat",
        ),
        migrations.DeleteModel(
            name="Hall",
        ),
    ]
