from django.core.exceptions import ValidationError
from django.db import models

from apps.shared.models import AbstractBaseModel


class Order(AbstractBaseModel):
    user = models.ForeignKey("BotUsers", on_delete=models.CASCADE)
    concert = models.ForeignKey("Concert", on_delete=models.CASCADE)
    concert_seats = models.ManyToManyField("ConcertSeat")
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.concert_seats.count() > 50:
            raise ValidationError(
                "You cannot purchase more than 50 tickets for a single concert."
            )

    def save(self, *args, **kwargs):
        self.total_price = sum(cs.seat.price for cs in self.concert_seats.all())
        for concert_seat in self.concert_seats.all():
            concert_seat.is_sold = True
            concert_seat.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.user} - {self.concert.name}, Total: {self.total_price}"
