from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET


@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    """Inizializza il cookie CSRF per il client Vue same-origin."""
    return JsonResponse({"detail": "CSRF cookie set"})


@require_GET
def healthz_view(request):
    """Healthcheck del backend non dipendente dal database."""
    return JsonResponse({"status": "ok"})


def api_404_view(request, exception=None):
    return JsonResponse({"detail": "Not found"}, status=404)
