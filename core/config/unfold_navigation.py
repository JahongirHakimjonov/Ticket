from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Foydalanuvchilar"),
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Bot foydalanuvchilari"),
                "icon": "person_add",
                "link": reverse_lazy("admin:ticket_botusers_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_botusers"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Konsertlar"),
        "items": [
            {
                "title": _("Konsertlar"),
                "icon": "theater_comedy",
                "link": reverse_lazy("admin:ticket_concert_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_concert"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Tushumlar"),
        "items": [
            {
                "title": _("Buyurtmalar"),
                "icon": "shopping_cart",
                "link": reverse_lazy("admin:ticket_order_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_order"
                ),
            },
            {
                "title": _("Xayriya"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:ticket_donate_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_donate"
                ),
            },
            {
                "title": _("Biletlar"),
                "icon": "confirmation_number",
                "link": reverse_lazy("admin:ticket_ticket_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_ticket"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Payme"),
        "items": [
            {
                "title": _("Transaksiyalar"),
                "icon": "receipt_long",
                "link": reverse_lazy(
                    "admin:payme_merchanttransactionsmodel_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_merchanttransactionsmodel"
                ),
            },
            {
                "title": _("Buyurtmalar"),
                "icon": "payments",
                "link": reverse_lazy("admin:payment_payment_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_payment"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Ma'lumotlar"),
        "items": [
            {
                "title": _("Ma'lumotlar"),
                "icon": "info",
                "link": reverse_lazy("admin:ticket_info_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_info"
                ),
            },
        ],
    },
]
