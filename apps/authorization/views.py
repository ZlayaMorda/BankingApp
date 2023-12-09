from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.views import View
from apps.authorization.forms import UserSignUpForm, UserSignInForm, CodeForm
from apps.authorization.services.code_generation import Code
from apps.authorization.services.custom_jwt import CustomJwt
from apps.authorization.services.send_auth_email import AuthEmail


def user_sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")
    else:
        form = UserSignUpForm()
    return render(request, "authorization/sign_up.html", {"form": form})


def user_sign_in(request):
    auth_email_service = AuthEmail()
    User = get_user_model()

    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            passport_id = form.cleaned_data["passport_identifier"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.filter(passport_identifier=passport_id).first()
                if check_password(user.password, password):
                    return render(request, "authorization/sign_in.html",
                                  {"state": "Invalid password or identifier", "form": form}, status=401)

                jwt_token = CustomJwt.generate_jwt(user)
                code = Code().store(jwt_token)
                url = request.build_absolute_uri('/auth/sign-in-code/')
                auth_email_service.send_login_mail(code, url=url, to_email=[user.email])

                return redirect("sign_in_code")

            except Exception as e:
                return render(request, "authorization/sign_in.html",
                              {"state": "Invalid password or identifier", "form": form}, status=401)
        else:
            return render(request, "authorization/sign_in.html",
                          {"form": form}, status=401)
    else:
        form = UserSignInForm()
        return render(request, "authorization/sign_in.html", {"form": form})


def user_sign_in_code(request):
    response = HttpResponseRedirect("/")

    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            jwt_token = Code().load(code)

            if jwt_token is not None:
                CustomJwt.set_cookie_jwt(response, jwt_token)
                return response
            else:
                return render(request, "authorization/sign_in_code.html", {"form": form, "state": "Invalid code"})
        else:
            return render(request, "authorization/sign_in_code.html", {"form": form, "state": "Invalid code"})
    form = CodeForm()
    return render(request, "authorization/sign_in_code.html", {"form": form})


class LogoutView(View):
    response = HttpResponseRedirect("/")

    def get(self, request):
        self.response.delete_cookie("jwt_token")
        return self.response
