from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Custom"),
        "items": [
            {
                "title": _("Users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_user_changelist"),
            },
            {
                "title": _("Bot users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:ticket_botusers_changelist"),
            },
            {
                "title": _("Groups"),
                "icon": "diversity_3",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
        ],
    },
]
