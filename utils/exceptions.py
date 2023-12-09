from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except AuthException as e:
            # response = HttpResponse(status=e.status_code, context={"message": e.message}, content="error.html")
            return render(request, "error/auth_error.html", {"message": e.message})
        except NotFound as e:
            return render(request, "error/error.html", {"message": e.message})
        except Exception as e:
            response = HttpResponseServerError("Oops! Something went wrong.")

        return response


class AuthException(BaseException):
    status_code = 401

    def __init__(self, message="Authentication exception"):
        self.message = message


class NotFound(BaseException):
    status_code = 404

    def __init__(self, message="Not found"):
        self.message = message
