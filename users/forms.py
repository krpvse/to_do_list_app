from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'registration-email-field',
        'placeholder': 'e-mail',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'registration-password-set-field',
        'placeholder': 'пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'registration-password-confirm-field',
        'placeholder': 'пароль',
    }))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = False


class UserAuthorizationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'authorization-email-field',
        'placeholder': 'e-mail',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'authorization-password-field',
        'placeholder': 'пароль',
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'password-reset-email-field',
            'placeholder': 'e-mail',
        }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='введите',
        widget=forms.PasswordInput(attrs={
            'class': 'password-reset-confirm-password-set-field',
            'placeholder': 'новый пароль',
        }))

    new_password2 = forms.CharField(
        label='подтвердите',
        widget=forms.PasswordInput(attrs={
            'class': 'password-reset-confirm-password-confirm-field',
            'placeholder': 'новый пароль',
        }))
