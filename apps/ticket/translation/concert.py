from modeltranslation.translator import TranslationOptions, register

from apps.ticket.models import Concert


@register(Concert)
class ConcertTranslationOptions(TranslationOptions):
    fields = ("name", "title", "description", "address")
