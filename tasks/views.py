from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from common.views import get_task_type, get_template_name
from tasks.forms import TaskForm
from tasks.models import Task


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        queryset = super(TasksListView, self).get_queryset()
        return queryset.filter(task_type=get_task_type(self.request.path), user=self.request.user).order_by('is_completed', '-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TasksListView, self).get_context_data()
        context['form'] = TaskForm()
        return context

    def get_template_names(self):
        return get_template_name(self.request.path)


@login_required
def add_task(request):
    title = request.POST['title']
    form = TaskForm(data=request.POST)
    if form.is_valid():
        Task.objects.create(title=title, task_type=get_task_type(request.META['HTTP_REFERER']), user=request.user)
    else:
        messages.error(request, 'Пишите задачи кратко. Не более 42 символов')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def change_task_status(request, task_id):
    task = Task.objects.get(id=task_id)
    is_completed = True if not task.is_completed else False
    Task.objects.filter(id=task_id).update(is_completed=is_completed)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_all_tasks(request):
    Task.objects.filter(task_type=get_task_type(request.META['HTTP_REFERER']), user=request.user).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
