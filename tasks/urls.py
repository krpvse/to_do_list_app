from django.urls import path

from tasks.views import tasks, change_task_status, delete_task, delete_all_tasks


app_name = 'tasks'

urlpatterns = [
    path('personal/', tasks, name='personal_tasks'),
    path('work/', tasks, name='work_tasks'),
    path('personal/page/<int:page_number>', tasks, name='personal_tasks_paginator'),
    path('work/page/<int:page_number>', tasks, name='work_tasks_paginator'),

    path('change_task_status/<int:task_id>', change_task_status, name='change_task_status'),
    path('delete_task/<int:task_id>', delete_task, name='delete_task'),
    path('delete_all_tasks/', delete_all_tasks, name='delete_all_tasks'),
]
