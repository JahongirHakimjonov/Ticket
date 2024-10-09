import os
import uuid

import qrcode
from PIL import Image, ImageDraw, ImageFont
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.core.files.base import ContentFile

from apps.ticket.models import Ticket, Order


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def generate_ticket_qr_code(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        for seat_number in order.seat_numbers.all():
            ticket_id = str(f"{order_id}_{uuid.uuid4()}")
            ticket_id_url = (
                f"{os.getenv('BASE_URL')}/admin/ticket/ticket/?q={ticket_id}"
            )

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(ticket_id_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            background = Image.open("static/image/ticket.png")
            background = background.resize((720, 1280))

            qr_image = qr_image.resize((343, 343))
            background.paste(qr_image, (65, 779))

            draw = ImageDraw.Draw(background)
            font_size = 16
            font = ImageFont.truetype("static/fonts/Roboto-Regular.ttf", font_size)

            type_position = (545, 820)
            row_position = (495, 950)
            seat_position = (555, 1087)

            draw.text(
                type_position,
                f"{order.seat.type.name_uz}",
                font=font,
                fill="black",
                align="center",
            )
            draw.text(
                row_position,
                f"{order.seat.name_uz}",
                font=font,
                fill="black",
                align="center",
            )
            draw.text(
                seat_position,
                f"{seat_number.number}",
                font=font,
                fill="black",
                align="center",
            )

            qr_code_path = f"media/tickets/{ticket_id}.png"
            background.save(qr_code_path)

            Ticket.objects.create(
                order=order,
                ticket_id=ticket_id,
                ticket_id_url=ticket_id_url,
                ticket=ContentFile(
                    open(qr_code_path, "rb").read(), name=f"{ticket_id}.png"
                ),
                seat=f"Joylashuv / Расположение: {order.seat.type.name} \nQator / Ряд: {order.seat.name} \nJoy / Место: {seat_number.number}",
                seat_id=order.seat,
                seat_number=seat_number,
            )
            seat_number.is_active = False
            seat_number.save()
    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
    except Exception as exc:
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            print(f"Max retries exceeded for order id {order_id}")
