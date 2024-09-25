from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


def handler404(request, *args, **argv):  # noqa
    response = render(request, "exceptions/404.html", {})
    response.status_code = 404
    return response


def handler400(request, *args, **argv):  # noqa
    response = render(request, "exceptions/400.html", {})
    response.status_code = 400
    return response


def handler403(request, *args, **argv):  # noqa
    response = render(request, "exceptions/403.html", {})
    response.status_code = 403
    return response


def handler500(request, *args, **argv):  # noqa
    response = render(request, "exceptions/500.html", {})
    response.status_code = 500
    return response


def handler502(request, *args, **argv):  # noqa
    response = render(request, "exceptions/502.html", {})
    response.status_code = 502
    return response
