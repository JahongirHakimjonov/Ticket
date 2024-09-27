from django.urls import path

from apps.payment.views import PaymeCallBackAPIView

urlpatterns = [
    path("merchant/payme/", PaymeCallBackAPIView.as_view()),
]
