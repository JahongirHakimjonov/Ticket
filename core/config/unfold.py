from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import unfold_navigation as navigation

UNFOLD = {
    "SITE_TITLE": "Django Default",
    "SITE_HEADER": "Django Default",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/felix.png"),
        "dark": lambda request: static("images/felix.png"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/favicon.ico"),
        },
    ],
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "environment_callback",
    "LOGIN": {
        "image": lambda request: static("images/login.jpg"),
    },
    "STYLES": [
        lambda request: static("css/tailwind.css"),
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "65 144 176",
            "100": "65 144 176",
            "200": "65 144 176",
            "300": "65 144 176",
            "400": "65 144 176",
            "500": "65 144 176",
            "600": "65 144 176",
            "700": "65 144 176",
            "800": "65 144 176",
            "900": "65 144 176",
            "950": "65 144 176",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
    "TABS": [
        {
            "models": [
                "ticket.concert",
                "ticket.seat",
                "ticket.seatnumber",
                "ticket.seattype",
            ],
            "items": [
                {
                    "title": _("Konsertlar"),
                    "link": reverse_lazy("admin:ticket_concert_changelist"),
                },
                {
                    "title": _("Qatorlar"),
                    "link": reverse_lazy("admin:ticket_seat_changelist"),
                },
                {
                    "title": _("O'rindiqlar"),
                    "link": reverse_lazy("admin:ticket_seatnumber_changelist"),
                },
                {
                    "title": _("Qator turlari"),
                    "link": reverse_lazy("admin:ticket_seattype_changelist"),
                },
            ],
        },
    ],
}


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "danger"]
