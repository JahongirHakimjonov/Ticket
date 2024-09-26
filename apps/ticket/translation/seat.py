from modeltranslation.translator import TranslationOptions, register

from apps.ticket.models import Seat


@register(Seat)
class SeatTranslationOptions(TranslationOptions):
    fields = ("name",)
