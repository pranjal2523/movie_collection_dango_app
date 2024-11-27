import threading
from django.http import JsonResponse
from django.views import View
from movies.models import RequestCounter


class RequestCounterMiddleware:
    _lock = threading.Lock()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment the request count for every request
        with self._lock:
            RequestCounter.objects.create(user=request.user if request.user.is_authenticated else None)
        return self.get_response(request)

    @classmethod
    def get_count(cls):
        # Returns the total count of requests in the database
        return RequestCounter.objects.count()

    @classmethod
    def reset_count(cls):
        # Delete all records in RequestCounter to reset count
        RequestCounter.objects.all().delete()
