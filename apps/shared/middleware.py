# middleware.py
from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class CustomErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            if isinstance(exception, Http404):
                return render(request, "exceptions/404.html", status=404)
            elif isinstance(exception, PermissionDenied):
                return render(request, "exceptions/403.html", status=403)
            elif isinstance(exception, SuspiciousOperation):
                return render(request, "exceptions/400.html", status=400)
            else:
                return render(request, "exceptions/500.html", status=500)
