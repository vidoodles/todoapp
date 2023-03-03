from rest_framework import generics, permissions
from .models import TodoList, TodoItem
from .serializers import (
    TodoListReadSerializer, 
    TodoListWriteSerializer, 
    TodoItemReadSerializer, 
    TodoItemWriteSerializer
)
from .utils import check_user_auth
from drf_yasg.utils import swagger_auto_schema

import logging

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

