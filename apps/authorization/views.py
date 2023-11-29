from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserSignUpForm, UserSignInForm


# Create your views here.


def user_sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")
    else:
        form = UserSignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def user_sign_in(request):
    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            passport_id = form.cleaned_data["passport_identifier"]
            password = form.cleaned_data["password"]
            # TODO get user email, create JWT, put in Redis

            return redirect("sign_in_code")
    else:
        form = UserSignInForm()
    return render(request, "sign_in.html", {"form": form})


def user_sign_in_code(request):
    return HttpResponse("Code")
