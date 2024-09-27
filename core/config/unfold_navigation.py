from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
            },
            {
                "title": _("Bot foydalanuvchilari"),
                "icon": "person_add",
                "link": reverse_lazy("admin:ticket_botusers_changelist"),
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
            },
            {
                "title": _("Xayriya"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:ticket_donate_changelist"),
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
            },
            {
                "title": _("Buyurtmalar"),
                "icon": "payments",
                "link": reverse_lazy("admin:payment_payment_changelist"),
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
            },
        ],
    },
]
