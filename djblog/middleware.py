import time
from django.core.cache import cache
from django.http import HttpResponse

class LoginRateLimitMiddleware:
    """
    Middleware to rate limit requests to login and admin authentication endpoints.
    Protects against brute-force password guessing and credential stuffing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Target login POST requests to admin or auth views
        if request.method == 'POST' and ('login' in request.path or request.path.startswith('/admin/')):
            ip = self.get_client_ip(request)
            cache_key = f"login_attempts_{ip}"
            attempts = cache.get(cache_key, 0)

            MAX_ATTEMPTS = 5
            TIMEOUT_SECONDS = 300  # 5 minutes lockout

            if attempts >= MAX_ATTEMPTS:
                return HttpResponse(
                    "Too many login attempts. Please wait 5 minutes before trying again.",
                    status=429
                )

            # Record attempt
            cache.set(cache_key, attempts + 1, TIMEOUT_SECONDS)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
