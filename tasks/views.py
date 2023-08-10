from django.shortcuts import render, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse

from tasks.forms import TaskForm
from tasks.models import Task


def tasks(request, page_number=1):
    if 'personal' in request.path:
        html_path = 'tasks/personal-tasks.html'
        task_type = 'Личная'
    else:
        html_path = 'tasks/work-tasks.html'
        task_type = 'Рабочая'

    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            title = request.POST['title']
            Task.objects.create(title=title, task_type=task_type, user=request.user)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    form = TaskForm()
    tasks = Task.objects.filter(task_type=task_type, user=request.user)

    per_page = 5
    paginator = Paginator(tasks, per_page)
    tasks_paginator = paginator.page(page_number)

    context = {'form': form,
               'tasks': tasks_paginator,
               }
    return render(request, html_path, context)


def change_task_status(request, task_id):
    task = Task.objects.get(id=task_id)
    if not task.is_completed:
        Task.objects.filter(id=task_id).update(is_completed=True)
    else:
        Task.objects.filter(id=task_id).update(is_completed=False)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_all_tasks(request):
    if 'personal' in (request.META['HTTP_REFERER']):
        Task.objects.filter(task_type='Личная', user=request.user).delete()
        return HttpResponseRedirect(reverse('tasks:personal_tasks'))
    else:
        Task.objects.filter(task_type='Рабочая', user=request.user).delete()
        return HttpResponseRedirect(reverse('tasks:work_tasks'))
