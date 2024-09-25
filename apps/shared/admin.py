# Register your models here.


from django.contrib import admin
from django.contrib.auth.models import Group, User

from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    def has_add_permission(self, request):
        return False


@admin.register(User)
class UserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("username",)
    list_editable = ("is_active", "is_staff", "is_superuser")
    actions = ["make_active", "make_inactive"]
    filter_vertical = ("groups", "user_permissions")

    def make_active(self, request, queryset):  # noqa
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):  # noqa
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"

    def has_add_permission(self, request):
        return False
