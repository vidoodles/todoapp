from rest_framework import generics, permissions
from .models import TodoList, TodoItem
from .serializers import (
    TodoListReadSerializer,
    TodoListWriteSerializer,
    TodoItemReadSerializer,
    TodoItemWriteSerializer
)
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import check_user_auth
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TodoListForm, TodoItemForm
from django.conf import settings

import requests
import logging
import json

logger = logging.getLogger(__name__)


class TodoListCreateView(generics.CreateAPIView):
    """
    API view for creating a new TodoList instance.
    Only authenticated users are allowed to create TodoLists.
    """
    serializer_class = TodoListWriteSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        """
        Sets the created_by field of the new TodoList to the user making the request.
        """
        # Check if user is not anonymous
        user = check_user_auth(self.request.user)
        if user:
            serializer.save(created_by=self.request.user)


class TodoListView(generics.ListAPIView):
    """
    API view for retrieving a list of all TodoLists created by the current user.
    Only authenticated users are allowed to create TodoLists.
    """
    serializer_class = TodoListReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """
        Returns a QuerySet containing all TodoLists created by the current user.
        """
        return TodoList.objects.all()


class TodoListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating or deleting a specific TodoList instance.
    Only authenticated users who created the TodoList are allowed to perform any operations.
    """
    serializer_class = TodoListWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Returns a QuerySet containing the TodoList instance requested by the user.
        """
        # Check if user is not anonymous
        user = check_user_auth(self.request.user)
        if user:
            return TodoList.objects.filter(created_by=user)


class TodoItemCreateView(generics.CreateAPIView):
    """
    API view for creating a new TodoItem instance.

    Only authenticated users are allowed to create TodoItems.
    """
    serializer_class = TodoItemWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Sets the todo_list field of the new TodoItem to the corresponding TodoList instance.
        """
        todo_list = None
        if self.kwargs.get('todo_list_id'):
            todo_list_id = self.kwargs['todo_list_id']
            todo_list = TodoList.objects.get(id=todo_list_id)
            if not todo_list:
                raise ValueError('Todo List does not exist')
        serializer.save(todo_list=todo_list)


class TodoItemListView(generics.ListAPIView):
    """
    API view for retrieving a list of all TodoItems in a specific TodoList.

    Authentication is not required for this endpoint.
    """
    swagger_fake_view = True
    serializer_class = TodoItemReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """
        Returns a QuerySet containing all TodoItems in the requested TodoList.
        """
        todo_list = TodoList.objects.get(id=self.kwargs['todo_list_id'])
        if not todo_list:
            raise ValueError('Todo List does not exist')
        todo_list = TodoItem.objects.filter(todo_list=todo_list)
        return todo_list


class TodoItemView(generics.ListAPIView):
    """
    API view for retrieving a list of all TodoLists created by the current user.
    Only authenticated users are allowed to create TodoLists.
    """
    serializer_class = TodoItemReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """
        Returns a QuerySet containing all TodoLists created by the current user.
        """
        return TodoItem.objects.all()


class TodoItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating or deleting a specific TodoItem instance.

    Only authenticated users are allowed to perform any operations.
    """
    serializer_class = TodoItemWriteSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """
        Returns a QuerySet containing the TodoList instance requested by the user.
        """
        user = check_user_auth(self.request.user)
        if user:
            return TodoItem.objects.filter(todo_list__created_by=user)

# Front end views


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                request.session['access_token'] = access_token
                request.session['is_authenticated'] = True
                request.session['username'] = username
                return redirect('my-list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session['is_authenticated'] = False 
    logout(request)
    return redirect('login')


def todo_list(request):
    serializer_class = TodoListReadSerializer
    permission_classes = (permissions.AllowAny,)
    lists = requests.get(f"{settings.BASE_URL}/todolist/")
    return render(
        request,
        'todolist/list.html',
        {'lists': lists.json(), 'token': request.session['access_token']}
    )


def todo_detail(request, list_id):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    items = TodoItem.objects.filter(list=todo_list)
    return render(request, 'todo/detail.html', {'list': todo_list, 'items': items})


def todo_create(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            jwt_token = request.session['access_token']
            url = f"{settings.BASE_URL}/todolist/create/"
            authorization = f"JWT {jwt_token}"
            headers = {'Authorization': authorization}
            result = requests.post(url, data=request.POST, headers=headers)
            if result.ok:
                return redirect('my-list')
    else:
        form = TodoListForm()
    return render(request, 'todolist/create.html', {'form': form})


def todo_edit(request, list_id):
    headers = {'Authorization': f"JWT {request.session['access_token']}"}
    url = f"{settings.BASE_URL}/todolist/{list_id}/"
    lists = requests.get(url=url, headers=headers)
    if request.method == 'POST':
        result = requests.put(url=url, data=request.POST, headers=headers)
        if result.ok:
            return redirect('my-list')
    else:
        form = TodoListForm()
    return render(request, 'todolist/edit.html', {'form': form, 'data': json.loads(lists.text)})


def todo_delete(request, list_id):
    if request.method == 'POST':
        jwt_token = request.session['access_token']
        url = f"{settings.BASE_URL}/todolist/{list_id}/"
        authorization = f"JWT {jwt_token}"
        headers = {'Authorization': authorization}
        result = requests.delete(url, headers=headers)
        if result.ok:
            return redirect('my-list')
    else:
        return render(request, 'todolist/delete.html')


def todo_item_create(request, list_id):
    headers = {'Authorization': f"JWT {request.session['access_token']}"}
    url = f"{settings.BASE_URL}/todolist/{list_id}/"
    lists = requests.get(url=url, headers=headers)
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        result = requests.post(
            url=f"{settings.BASE_URL}/todolist/{list_id}/items/create/", 
            data=request.POST, 
            headers=headers
        )
        if result.ok:
            return redirect('my-list')
    else:
        form = TodoItemForm()
    return render(request, 'todoitem/create.html', {'list': todo_list, 'form': form})


def todo_item_edit(request, item_id):
    headers = {'Authorization': f"JWT {request.session['access_token']}"}
    url = f"{settings.BASE_URL}/todoitems/{item_id}/"
    lists = requests.get(url=url, headers=headers)
    if request.method == 'POST':
        result = requests.put(url=url, data=request.POST, headers=headers)
        if result.ok:
            return redirect('my-list')
    else:
        form = TodoItemForm(json.loads(lists.text))
    return render(request, 'todoitem/edit.html', {'item_id': item_id, 'form': form})


def todo_item_delete(request, item_id):
    if request.method == 'POST':
        jwt_token = request.session['access_token']
        url = f"{settings.BASE_URL}/todoitems/{item_id}/"
        authorization = f"JWT {jwt_token}"
        headers = {'Authorization': authorization}
        result = requests.delete(url, headers=headers)
        if result.ok:
            return redirect('my-list')
    else:
        return render(request, 'todoitem/delete.html')
