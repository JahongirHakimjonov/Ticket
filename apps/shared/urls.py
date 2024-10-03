from django.urls import path

from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]

handler404 = "apps.shared.views.handler404"
handler400 = "apps.shared.views.handler400"
handler403 = "apps.shared.views.handler403"
handler500 = "apps.shared.views.handler500"
handler502 = "apps.shared.views.handler502"
