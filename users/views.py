from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages

from users.forms import UserRegistrationForm, UserAuthorizationForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/index.html')
    else:
        return HttpResponseRedirect(reverse('tasks:personal_tasks'))


def authorization(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserAuthorizationForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('tasks:personal_tasks'))
        else:
            form = UserAuthorizationForm()
        context = {'form': form}
        return render(request, 'users/authorization.html', context)
    else:
        return HttpResponseRedirect(reverse('tasks:personal_tasks'))


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Поздравляем! Вы успешно зарегистрированы.\n'
                                          'Теперь заходите в профиль и планируйте задачи!')
                return HttpResponseRedirect(reverse('users:authorization'))
        else:
            form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'users/registration.html', context)
    else:
        return HttpResponseRedirect(reverse('tasks:personal'))


def recovery(request):
    if not request.user.is_authenticated:
        return render(request, 'users/recovery.html')
    else:
        return HttpResponseRedirect(reverse('tasks:personal'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
