from to_do_list.settings import PERSONAL_TASKS_ROUTE


def get_task_type(path):
    return 'Личная' if PERSONAL_TASKS_ROUTE in path else 'Рабочая'


def get_template_name(path):
    return 'tasks/personal-tasks.html' if PERSONAL_TASKS_ROUTE in path else 'tasks/work-tasks.html'
