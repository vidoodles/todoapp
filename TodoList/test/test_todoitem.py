from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from TodoList.models import TodoList, TodoItem
from datetime import datetime

import os


class TodoListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.todo_list = TodoList.objects.create(
            title='Test Todo List', created_by=self.user)
        self.item_data = {'description': 'Test Todo Item',
                          'due_date': datetime.today().strftime('%Y-%m-%d'), 'todo_list': self.todo_list.id}

    def test_create_item(self):
        response = self.client.post(reverse('create-item', kwargs={'todo_list_id': self.todo_list.id}),
                                    self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.assertEqual(TodoItem.objects.get().description, 'Test Todo Item')

    def test_retrieve_item_list(self):
        self.client.post(reverse(
            'create-item', kwargs={'todo_list_id': self.todo_list.id}), self.item_data, format='json')
        response = self.client.get(
            reverse('detail-list', kwargs={'pk': self.todo_list.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_item_detail(self):

        response = self.client.post(reverse('create-item', kwargs={'todo_list_id': self.todo_list.id}),
                                    self.item_data, format='json')
        item_id = response.data['id']
        response = self.client.get(
            reverse('detail-item', kwargs={'pk': item_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Todo Item')

    def test_update_item(self):
        del self.item_data["todo_list"]
        response = self.client.post(reverse('create-item', kwargs={'todo_list_id': self.todo_list.id}),
                                    self.item_data, format='json')
        item_id = response.data['id']
        updated_data = {'description': 'Updated Item description', 'due_date': datetime.today().strftime('%Y-%m-%d')}
        response = self.client.put(reverse('detail-item', kwargs={'pk': item_id}),
                                   updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated Item description')

    def test_delete_item(self):
        response = self.client.post(reverse('create-item', kwargs={'todo_list_id': self.todo_list.id}),
                                    self.item_data, format='json')
        item_id = response.data['id']
        response = self.client.delete(
            reverse('detail-item', kwargs={'pk': item_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TodoItem.objects.count(), 0)
