from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

from users.views import index
from users.forms import UserPasswordResetForm, UserSetPasswordForm


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('user/', include('users.urls', namespace='users')),
    path('tasks/', include('tasks.urls', namespace='tasks')),

    #django-default-password-reset
    path('user/password-reset/', PasswordResetView.as_view(
        template_name='users/password-reset.html',
        form_class=UserPasswordResetForm),
         name='password_reset'),
    path('user/password-reset-done/', PasswordResetDoneView.as_view(
        template_name='users/password-reset-done.html'),
         name='password_reset_done'),
    path('user/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password-reset-confirm.html',
        success_url=reverse_lazy("users:authorization"),
        form_class=UserSetPasswordForm),
         name='password_reset_confirm'),
]