from django.urls import path

from users.views import authorization, registration, recovery, logout


app_name = 'users'

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('registration/', registration, name='registration'),
    path('recovery/', recovery, name='recovery'),
    path('logout/', logout, name='logout'),
]
