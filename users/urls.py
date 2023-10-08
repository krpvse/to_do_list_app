from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLoginView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('authorization/', UserLoginView.as_view(), name='authorization'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


