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
            {
                "title": _("Guruhlar"),
                "icon": "diversity_3",
                "link": reverse_lazy("admin:auth_group_changelist"),
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
        "title": _("Zallar"),
        "items": [
            {
                "title": _("Zallar"),
                "icon": "stadium",
                "link": reverse_lazy("admin:ticket_hall_changelist"),
            },
            {
                "title": _("O'rindiqlar"),
                "icon": "airline_seat_recline_normal",
                "link": reverse_lazy("admin:ticket_seat_changelist"),
            },
            {
                "title": _("Konsertlar o'rindiqlari"),
                "icon": "event_seat",
                "link": reverse_lazy("admin:ticket_concertseat_changelist"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Buyurtmalar"),
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
