from django.urls import path

from tasks.views import change_task_status, delete_task, delete_all_tasks, add_task, TasksListView


app_name = 'tasks'

urlpatterns = [
    path('personal/', TasksListView.as_view(), name='personal_tasks'),
    path('work/', TasksListView.as_view(), name='work_tasks'),
    path('personal/<int:page>', TasksListView.as_view(), name='personal_tasks_paginator'),
    path('work/<int:page>', TasksListView.as_view(), name='work_tasks_paginator'),

    path('<str:tasks_type>/add-task/', add_task, name='add_task'),
    path('<str:tasks_type>/change-task-status/<int:task_id>', change_task_status, name='change_task_status'),
    path('<str:tasks_type>/delete-task/<int:task_id>', delete_task, name='delete_task'),
    path('<str:tasks_type>/delete-all-tasks/', delete_all_tasks, name='delete_all_tasks'),
]
