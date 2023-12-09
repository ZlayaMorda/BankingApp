from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from apps.users.models import CustomUser


class UserSignUpForm(BaseUserCreationForm):
    first_name = forms.CharField(max_length=50, help_text="First name")
    last_name = forms.CharField(max_length=50, help_text="Last name")
    passport_identifier = forms.CharField(max_length=14, help_text="Passport identifier 0000000A000AA0")
    email = forms.EmailField(max_length=254, help_text="email@em.mail")

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2")


class UserSignInForm(forms.Form):
    passport_identifier = forms.CharField(max_length=14, help_text="Passport identifier 0000000A000AA0")
    password = forms.CharField(widget=forms.PasswordInput)
