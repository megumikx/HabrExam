from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )

        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта")

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data

        user = User.objects.filter(email=email).first()

        if user is None:
            raise forms.ValidationError("Пользователь с такой почтой не найден.")

        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is None:
            raise forms.ValidationError("Неверный пароль.")

        self.user = authenticated_user

        return cleaned_data
