from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


def handler404(request, exception):  # noqa
    return render(request, "exceptions/404.html", status=404)


def handler400(request, exception):  # noqa
    return render(request, "exceptions/400.html", status=400)


def handler403(request, exception):  # noqa
    return render(request, "exceptions/403.html", status=403)


def handler500(request):  # noqa
    return render(request, "exceptions/500.html", status=500)


def handler502(request, exception):  # noqa
    return render(request, "exceptions/502.html", status=502)
