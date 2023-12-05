from .services.custom_jwt import CustomJwt


class AdminJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = CustomJwt.get_user_from_token(request)
        if request.path.startswith("/admin/"):
            if user.role != "admin":
                # TODO exception
                raise Exception("Permission denied")

        request.user = user

        response = self.get_response(request)

        return response
