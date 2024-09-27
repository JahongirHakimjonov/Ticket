from django.db import models

from apps.shared.models import AbstractBaseModel


class Ticket(AbstractBaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")
    ticket_id = models.CharField(max_length=255, null=True, blank=False)
    ticket_id_url = models.URLField(max_length=255, null=True, blank=True)
    ticket = models.ImageField(upload_to="tickets/")
    seat = models.CharField(max_length=255, null=True, blank=False)
