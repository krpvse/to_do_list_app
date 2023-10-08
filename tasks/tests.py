from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task


class TasksListViewTestCase(TestCase):
    fixtures = ['users/fixtures/test_users.json', 'tasks/fixtures/test_tasks.json']

    def setUp(self):
        self.personal_tasks_path = reverse('tasks:personal_tasks')
        self.work_tasks_path = reverse('tasks:work_tasks')
        self.user = {
            'username': 'test_user@gmail.com',
            'password': '1234567Pp',
        }

    def test_get_personal_task_page(self):
        self.client.login(username=self.user['username'], password=self.user['password'])

        response = self.client.get(self.personal_tasks_path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/personal-tasks.html')

        self.assertEqual(
            list(response.context_data['object_list']),
            list(Task.objects.filter(user=2, task_type='Личная').order_by('is_completed', '-id')[:5])
        )

    def test_get_work_task_page(self):
        self.client.login(username=self.user['username'], password=self.user['password'])

        response = self.client.get(self.work_tasks_path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/work-tasks.html')

        self.assertEqual(
            list(response.context_data['object_list']),
            list(Task.objects.filter(user=2, task_type='Рабочая').order_by('is_completed', '-id')[:5])
        )

    def test_redirect_not_authenticated_user(self):
        response = self.client.get(self.personal_tasks_path)
        redirect_path = f'{reverse("users:authorization")}?next={self.personal_tasks_path}'
        self.assertRedirects(response, redirect_path)

        response = self.client.get(self.work_tasks_path)
        redirect_path = f'{reverse("users:authorization")}?next={self.work_tasks_path}'
        self.assertRedirects(response, redirect_path)


class TaskListChangeTestCase(TestCase):
    fixtures = ['users/fixtures/test_users.json', 'tasks/fixtures/test_tasks.json']

    def setUp(self):
        self.personal_tasks_path = reverse('tasks:personal_tasks')
        self.work_tasks_path = reverse('tasks:work_tasks')
        self.client.login(username='test_user@gmail.com', password='1234567Pp')
        self.length_error_message = 'Пишите задачи кратко. Не более 42 символов'

    def test_add_personal_task(self):
        response = self.client.get(self.personal_tasks_path)
        new_task = {'title': 'Test task'}
        self.assertNotContains(response, new_task['title'])

        path = reverse('tasks:add_task', kwargs={'tasks_type': response.wsgi_request.tasks_type})
        self.client.post(path, new_task)

        response = self.client.get(self.personal_tasks_path)
        self.assertContains(response, new_task['title'])

    def test_add_work_task(self):
        response = self.client.get(self.work_tasks_path)
        new_task = {'title': 'Test task'}
        self.assertNotContains(response, new_task['title'])

        path = reverse('tasks:add_task', kwargs={'tasks_type': response.wsgi_request.tasks_type})
        self.client.post(path, new_task)

        response = self.client.get(self.work_tasks_path)
        self.assertContains(response, new_task['title'])

    def test_change_personal_task_status(self):
        response = self.client.get(self.personal_tasks_path)
        self.assertFalse(Task.objects.get(id=7, title='Play computer game').is_completed)

        path = reverse('tasks:change_task_status', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
            'task_id': 7,
        })
        self.client.post(path)
        self.assertTrue(Task.objects.get(id=7, title='Play computer game').is_completed)

    def test_change_work_task_status(self):
        response = self.client.get(self.work_tasks_path)
        self.assertFalse(Task.objects.get(id=10, title='Get advice').is_completed)

        path = reverse('tasks:change_task_status', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
            'task_id': 10,
        })
        self.client.post(path)
        self.assertTrue(Task.objects.get(id=10, title='Get advice').is_completed)

    def test_delete_personal_task(self):
        response = self.client.get(self.personal_tasks_path)
        self.assertContains(response, 'Play computer game')

        path = reverse('tasks:delete_task', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
            'task_id': 7,
        })
        self.client.post(path)

        response = self.client.get(self.personal_tasks_path)
        self.assertNotContains(response, 'Play computer game')
        self.assertFalse(Task.objects.filter(id=7, title='Play computer game'))

    def test_delete_work_task(self):
        response = self.client.get(self.work_tasks_path)
        self.assertContains(response, 'Get advice')

        path = reverse('tasks:delete_task', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
            'task_id': 10,
        })
        self.client.post(path)

        response = self.client.get(self.work_tasks_path)
        self.assertNotContains(response, 'Get advice')
        self.assertFalse(Task.objects.filter(id=7, title='Get advice'))

    def test_delete_all_personal_tasks(self):
        response = self.client.get(self.personal_tasks_path)
        self.assertTrue(response.context_data['page_obj'].object_list)
        self.assertNotContains(response, 'У вас ещё нет задач')

        path = reverse('tasks:delete_all_tasks', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
        })
        self.client.post(path)

        response = self.client.get(self.personal_tasks_path)
        self.assertFalse(response.context_data['page_obj'].object_list)
        self.assertContains(response, 'У вас ещё нет задач')

    def test_delete_all_work_tasks(self):
        response = self.client.get(self.work_tasks_path)
        self.assertTrue(response.context_data['page_obj'].object_list)
        self.assertNotContains(response, 'У вас ещё нет задач')

        path = reverse('tasks:delete_all_tasks', kwargs={
            'tasks_type': response.wsgi_request.tasks_type,
        })
        self.client.post(path)

        response = self.client.get(self.work_tasks_path)
        self.assertFalse(response.context_data['page_obj'].object_list)
        self.assertContains(response, 'У вас ещё нет задач')

    def test_personal_task_title_length_error(self):
        response = self.client.get(self.personal_tasks_path)
        wrong_task = {'title': 'Very very very very very very very very very loooooooooooong task'}

        path = reverse('tasks:add_task', kwargs={'tasks_type': response.wsgi_request.tasks_type})
        self.client.post(path, wrong_task)

        response = self.client.get(self.personal_tasks_path)
        self.assertFalse(Task.objects.filter(title=wrong_task['title']))
        self.assertContains(response, self.length_error_message)

    def test_work_task_title_length_error(self):
        response = self.client.get(self.work_tasks_path)
        wrong_task = {'title': 'Very very very very very very very very very loooooooooooong task'}

        path = reverse('tasks:add_task', kwargs={'tasks_type': response.wsgi_request.tasks_type})
        self.client.post(path, wrong_task)

        response = self.client.get(self.work_tasks_path)
        self.assertFalse(Task.objects.filter(title=wrong_task['title']))
        self.assertContains(response, self.length_error_message)
