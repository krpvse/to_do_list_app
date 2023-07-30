from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages

from users.forms import UserRegistrationForm, UserAuthorizationForm


def index(request):
    return render(request, 'users/index.html')


def authorization(request):
    if request.method == 'POST':
        form = UserAuthorizationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserAuthorizationForm()
    context = {'form': form}
    return render(request, 'users/authorization.html', context)


def registration(request):
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


def recovery(request):
    return render(request, 'users/recovery.html')

