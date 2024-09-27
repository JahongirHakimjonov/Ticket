from django.urls import path

from apps.payme.views import MerchantAPIView


urlpatterns = [path("merchant/", MerchantAPIView.as_view())]
