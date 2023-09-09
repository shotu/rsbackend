from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.functional import SimpleLazyObject

def basic_auth_middleware(get_response):
    def middleware(request):
        # Check if the Authorization header is present
        if 'HTTP_AUTHORIZATION' in request.META:
            # Split the Authorization header to get the username and password
            auth_type, auth_string = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if auth_type == 'Basic':
                username, password = auth_string.strip().decode('base64').split(':', 1)
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    # If authentication is successful, set the user in the request
                    request.user = SimpleLazyObject(lambda: user)

        response = get_response(request)
        return response

    return middleware
