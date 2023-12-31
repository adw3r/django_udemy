from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User
from users.tasks import send_email_verif


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'}
        )
    )

    class Meta:
        model = User
        fields = 'username', 'password'


class UserRegForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя'}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите почту'}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-4', 'placeholder': 'Подтверждение пароля'}
        )
    )

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password1', 'password2'

    def save(self, commit=True):
        user = super().save(commit=commit)
        send_email_verif.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4'}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-4', 'readonly': True}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'readonly': True}, )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'custom-file-input'}
        ), required=False

    )

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'image'
