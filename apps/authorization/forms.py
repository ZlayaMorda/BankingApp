from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from apps.authorization.services.validators import only_int, valid_identifier
from apps.users.models import CustomUser


class UserSignUpForm(BaseUserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    passport_identifier = forms.CharField(max_length=14, validators=[valid_identifier],
                                          help_text="Passport identifier 0000000A000AA0")
    email = forms.EmailField(max_length=254, help_text="email@em.mail")

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2")


class UserSignInForm(forms.Form):
    passport_identifier = forms.CharField(max_length=14, validators=[valid_identifier],
                                          help_text="Passport identifier 0000000A000AA0")
    password = forms.CharField(widget=forms.PasswordInput)


class CodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, validators=[only_int])
