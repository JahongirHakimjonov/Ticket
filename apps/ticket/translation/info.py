from modeltranslation.translator import TranslationOptions, register

from apps.ticket.models import Info


@register(Info)
class InfoTranslationOptions(TranslationOptions):
    fields = ("name", "description")
