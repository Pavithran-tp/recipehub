from django.utils import timezone

class CustomTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.timezone:
            user_timezone = request.user.timezone
            request.session['django_timezone'] = user_timezone
            timezone.activate(user_timezone)
        elif request.session.get('django_timezone'):
            timezone.activate(request.session['django_timezone'])
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
