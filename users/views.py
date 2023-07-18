from django.shortcuts import render


def index(request):
    return render(request, 'users/index.html')


def authorization(request):
    return render(request, 'users/authorization.html')


def registration(request):
    return render(request, 'users/registration.html')


def recovery(request):
    return render(request, 'users/recovery.html')

