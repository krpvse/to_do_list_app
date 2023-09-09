from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserRegistrationForm, UserAuthorizationForm, UserPasswordResetForm, UserSetPasswordForm


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
    success_url = reverse_lazy('tasks:personal_tasks')
    success_message = f'Поздравляем! Вы успешно зарегистрированы.\nТеперь заходите в профиль и планируйте задачи!'


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password-reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('index')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password-reset-confirm.html'
    success_url = reverse_lazy('users:authorization')
    form_class = UserSetPasswordForm



#function-based-views

# def registration(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = UserRegistrationForm(data=request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Поздравляем! Вы успешно зарегистрированы.\n'
#                                           'Теперь заходите в профиль и планируйте задачи!')
#                 return HttpResponseRedirect(reverse('users:authorization'))
#         else:
#             form = UserRegistrationForm()
#         context = {'form': form}
#         return render(request, 'users/registration.html', context)
#     else:
#         return HttpResponseRedirect(reverse('tasks:personal'))


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'users/index.html')
#     else:
#         return HttpResponseRedirect(reverse('tasks:personal_tasks'))


# def authorization(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = UserAuthorizationForm(data=request.POST)
#             if form.is_valid():
#                 username = request.POST['username']
#                 password = request.POST['password']
#                 user = auth.authenticate(username=username, password=password)
#                 if user:
#                     auth.login(request, user)
#                     return HttpResponseRedirect(reverse('tasks:personal_tasks'))
#         else:
#             form = UserAuthorizationForm()
#         context = {'form': form}
#         return render(request, 'users/authorization.html', context)
#     else:
#         return HttpResponseRedirect(reverse('tasks:personal_tasks'))
