from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_index_get(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/index.html')


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.user = {
            'username': 'test_user@gmail.com',
            'password1': '1234567Pp',
            'password2': '1234567Pp',
        }
        self.error_message = 'Введенные пароли не совпадают'
        self.success_message = 'Поздравляем! Вы успешно зарегистрированы'

    def test_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_post(self):
        self.assertFalse(User.objects.filter(username=self.user['username']).exists())

        response = self.client.post(self.path, self.user)

        self.assertTrue(User.objects.filter(username=self.user['username']).exists())
        self.assertRedirects(response, reverse('users:authorization'))

    def test_create_registration_success_message(self):
        self.client.post(self.path, self.user)
        self.assertTrue(User.objects.filter(username=self.user['username']).exists())

        response = self.client.get(reverse('users:authorization'))

        self.assertContains(response, self.success_message)

    def test_registration_post_error(self):
        wrong_user_data = {
            'username': 'test_user@gmail.com',
            'password1': 'SOMEWRONGPASSWORD',
            'password2': 'somewrongpassword',
        }

        response = self.client.post(self.path, wrong_user_data)

        self.assertTrue(response.context_data['form'].error_messages)
        self.assertContains(response, self.error_message)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:authorization')
        self.user = {
            'username': 'test_user@gmail.com',
            'password': '1234567Pp',
        }
        self.error_message = 'Пожалуйста, введите правильные имя пользователя и пароль. ' \
                             'Оба поля могут быть чувствительны к регистру.'

        User.objects.create_user(username=self.user['username'], password=self.user['password'])

    def test_authorization_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/authorization.html')

    def test_redirect_authenticated_user(self):
        response = self.client.get(self.path)

        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/authorization.html')

        self.client.login(username=self.user['username'], password=self.user['password'])

        response = self.client.get(self.path, follow=True)

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('tasks:personal_tasks'))
        self.assertTemplateUsed(response, 'tasks/personal-tasks.html')

    def test_authorization_post(self):
        response = self.client.post(self.path, self.user)

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('tasks:personal_tasks'))

    def test_authorization_post_error(self):
        wrong_user_data = {
            'username': 'test_user@gmail.com',
            'password': 'somewrongpassword',
        }

        response = self.client.post(self.path, wrong_user_data)

        self.assertTrue(response.context_data['form'].error_messages)
        self.assertContains(response, self.error_message)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/authorization.html')
