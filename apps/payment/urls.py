from django.urls import path

from apps.payment.views import PaymeCallBackAPIView

urlpatterns = [
    path("payme/", PaymeCallBackAPIView.as_view()),
]
