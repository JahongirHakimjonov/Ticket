from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import News


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")
