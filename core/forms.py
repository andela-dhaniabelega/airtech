import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.models import User


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2', 'photo')

    def clean_password2(self):
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if not re.match(password_pattern, password1):
                raise forms.ValidationError(
                    "Password must contain at least: "
                    "1 upper case letter, 1 lower case letter, 1 special character, 1 digit "
                    "and have a minimum 8 characters")
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email_pattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}" \
                        "[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        email = self.cleaned_data.get("email")
        if email and not re.match(email_pattern, email):
            raise forms.ValidationError("Invalid Email")


class ChangeUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'password', 'photo')
