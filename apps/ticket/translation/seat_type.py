from modeltranslation.translator import TranslationOptions, register

from apps.ticket.models import SeatType


@register(SeatType)
class SeatTranslationOptions(TranslationOptions):
    fields = ("name",)
