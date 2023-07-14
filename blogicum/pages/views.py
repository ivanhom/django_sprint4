from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """Вывод страницы информации."""
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Вывод страницы правил."""
    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    """Вывод кастомного шаблона при ошибке 403."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Вывод кастомного шаблона при ошибке 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request, *args, **kwargs):
    """Вывод кастомного шаблона при ошибке 500."""
    return render(request, 'pages/500.html', status=500)
