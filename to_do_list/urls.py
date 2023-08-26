from django.contrib import admin
from django.urls import path, include

from users.views import IndexView, UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='index'),
    path('user/', include('users.urls', namespace='users')),
    path('tasks/', include('tasks.urls', namespace='tasks')),

    path('user/password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('user/password-reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('user/password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
