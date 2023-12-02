from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .forms import UserSignUpForm, UserSignInForm, CodeForm
from .services.code_generation import Code
from .services.custom_jwt import CustomJwt


def user_sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")
    else:
        form = UserSignUpForm()
    return render(request, "sign_up.html", {"form": form})


def user_sign_in(request):
    User = get_user_model()
    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            passport_id = form.cleaned_data["passport_identifier"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.filter(passport_identifier=passport_id).first()
                if check_password(user.password, password):
                    return render(request, "sign_in.html",
                                  {"state": "Invalid password or identifier", "form": form}, status=401)
                # TODO CREATE EMAIL SENDING
                jwt_token = CustomJwt.generate_jwt(user)
                Code().store(jwt_token)

                return redirect("sign_in_code")

            except Exception as e:
                return render(request, "sign_in.html",
                              {"state": "Invalid password or identifier", "form": form}, status=401)
        else:
            return render(request, "sign_in.html",
                          {"form": form}, status=401)
    else:
        form = UserSignInForm()
        return render(request, "sign_in.html", {"form": form})


def user_sign_in_code(request):
    response = HttpResponseRedirect("/home/")

    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            jwt_token = Code().load(code)

            if jwt_token is not None:
                CustomJwt.set_cookie_jwt(response, jwt_token)
                return response
            else:
                return render(request, "sign_in_code.html", {"form": form, "state": "Invalid code"})
        else:
            return render(request, "sign_in_code.html", {"form": form, "state": "Invalid code"})
    form = CodeForm()
    return render(request, "sign_in_code.html", {"form": form})
