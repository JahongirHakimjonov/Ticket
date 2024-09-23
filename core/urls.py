from django.conf import settings
from django.conf.urls.i18n import i18n_patterns  # noqa: F401
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("apps.shared.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.shared.views.handler404"
handler400 = "apps.shared.views.handler400"
handler403 = "apps.shared.views.handler403"
handler500 = "apps.shared.views.handler500"
handler502 = "apps.shared.views.handler502"
