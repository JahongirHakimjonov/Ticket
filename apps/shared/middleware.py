# middleware.py
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class CustomErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            if isinstance(exception, Http404):
                return render(request, "exceptions/404.html", status=404)
