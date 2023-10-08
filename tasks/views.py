from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.views.generic.list import ListView

from common.views import get_redirect_path, get_task_type, get_template_name
from tasks.forms import TaskForm
from tasks.models import Task


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        queryset = super(TasksListView, self).get_queryset()
        user_queryset = queryset.filter(task_type=get_task_type(self.request.tasks_type),
                                        user=self.request.user)
        return user_queryset.order_by('is_completed', '-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TasksListView, self).get_context_data()
        context['form'] = TaskForm()
        return context

    def get_template_names(self):
        return get_template_name(self.request.path)


@login_required
def add_task(request, tasks_type):
    title = request.POST['title']
    form = TaskForm(data=request.POST)
    if form.is_valid():
        Task.objects.create(title=title, task_type=get_task_type(tasks_type),
                            user=request.user)
    else:
        messages.error(request, 'Пишите задачи кратко. Не более 42 символов')

    return HttpResponseRedirect(get_redirect_path(tasks_type))


@login_required
def change_task_status(request, tasks_type, task_id):
    task = Task.objects.get(id=task_id)
    Task.objects.filter(id=task_id).update(is_completed=True if not task.is_completed else False)
    return HttpResponseRedirect(get_redirect_path(tasks_type))


@login_required
def delete_task(request, tasks_type, task_id):
    Task.objects.get(id=task_id).delete()
    return HttpResponseRedirect(get_redirect_path(tasks_type))


@login_required
def delete_all_tasks(request, tasks_type):
    Task.objects.filter(task_type=get_task_type(tasks_type), user=request.user).delete()
    return HttpResponseRedirect(get_redirect_path(tasks_type))
