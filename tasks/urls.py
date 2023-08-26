from django.urls import path

from tasks.views import change_task_status, delete_task, delete_all_tasks, TasksListView, add_task
from to_do_list.settings import PERSONAL_TASKS_ROUTE, WORK_TASKS_ROUTE

app_name = 'tasks'

urlpatterns = [
    path(PERSONAL_TASKS_ROUTE, TasksListView.as_view(), name='personal_tasks'),
    path(WORK_TASKS_ROUTE, TasksListView.as_view(), name='work_tasks'),
    path(f'{PERSONAL_TASKS_ROUTE}<int:page>', TasksListView.as_view(), name='personal_tasks_paginator'),
    path(f'{WORK_TASKS_ROUTE}<int:page>', TasksListView.as_view(), name='work_tasks_paginator'),

    path('add-task/', add_task, name='add_task'),
    path('change-task-status/<int:task_id>', change_task_status, name='change_task_status'),
    path('delete-task/<int:task_id>', delete_task, name='delete_task'),
    path('delete-all-tasks/', delete_all_tasks, name='delete_all_tasks'),
]
