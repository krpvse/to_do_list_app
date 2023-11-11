from django.contrib.auth.models import User
from django.contrib.auth.views import (LoginView, PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from users.forms import (UserAuthorizationForm, UserPasswordResetForm,
                         UserRegistrationForm, UserSetPasswordForm)


class IndexView(TemplateView):
    template_name = 'users/index.html'


class UserLoginView(LoginView):
    template_name = 'users/authorization.html'
    form_class = UserAuthorizationForm
    redirect_authenticated_user = True


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:authorization')
    success_message = f'Поздравляем! Вы успешно зарегистрированы.\n' \
                      f'Теперь заходите в профиль и планируйте задачи!'


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password-reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('index')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password-reset-confirm.html'
    success_url = reverse_lazy('users:authorization')
    form_class = UserSetPasswordForm
