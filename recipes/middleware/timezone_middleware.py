from django.utils import timezone


class CustomTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_timezone = request.session.get('django_timezone')
        if user_timezone:
            try:
                timezone.activate(user_timezone)
            except timezone.UnknownTimeZoneError:
                timezone.deactivate()
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
