from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export tickets to xlsx file."

    def handle(self, *args, **kwargs):
        from apps.ticket.models import Ticket
        import openpyxl

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(
            [
                "ID",
                "Buyurtmachi",
                "Buyurtmachi raqami",
                "Joylashuv",
            ]
        )

        for ticket in Ticket.objects.all():
            ws.append(
                [
                    ticket.id,
                    ticket.order.user.full_name,
                    ticket.order.user.phone,
                    ticket.seat,
                ]
            )

        wb.save("tickets.xlsx")
        self.stdout.write(self.style.SUCCESS("Tickets exported successfully."))
