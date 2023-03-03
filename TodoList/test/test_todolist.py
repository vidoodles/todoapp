from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from TodoList.models import TodoList, TodoItem
from datetime import datetime

import os


class TodoListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'))
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.todo_list = TodoList.objects.create(
            title='Test Todo List', created_by=self.user)

    def test_todo_list_create(self):
        url = reverse('create-list')
        data = {'title': 'New Todo List'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), 2)
        self.assertEqual(TodoList.objects.get(pk=response.data['id']).title, 'New Todo List')

    def test_todo_list_list(self):
        url = reverse('list-lists')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_todo_list_detail(self):
        url = reverse('detail-list', kwargs={'pk': self.todo_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.todo_list.title)

    def test_todo_list_update(self):
        url = reverse('detail-list', kwargs={'pk': self.todo_list.id})
        data = {'title': 'Updated Todo List Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo_list.refresh_from_db()
        self.assertEqual(self.todo_list.title, 'Updated Todo List Name')

    def test_todo_list_delete(self):
        url = reverse('detail-list', kwargs={'pk': self.todo_list.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TodoList.objects.count(), 0)
