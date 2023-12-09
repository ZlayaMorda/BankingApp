from .services.custom_jwt import CustomJwt
from django.shortcuts import redirect


class AdminJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            user = CustomJwt.get_user_from_token(request)
            if user.role != "admin":
                # TODO exception
                raise Exception("Permission denied")
            
        response = self.get_response(request)
        return response
