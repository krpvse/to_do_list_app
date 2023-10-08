from django.urls import reverse


def get_task_type(tasks_type):
    return 'Личная' if tasks_type == 'personal' else 'Рабочая'


def get_redirect_path(tasks_type):
    if tasks_type == 'personal':
        redirect_path = reverse('tasks:personal_tasks')
    else:
        redirect_path = reverse('tasks:work_tasks')
    return redirect_path


def get_template_name(path):
    return 'tasks/personal-tasks.html' if 'personal' in path else 'tasks/work-tasks.html'
