from rest_framework import serializers
from .models import TodoList, TodoItem

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'description', 'due_date', 'completed')

class TodoListWriteSerializer(serializers.ModelSerializer):
    todoitem_set = TodoItemSerializer(many=True,  read_only=True)

    class Meta:
        model = TodoList
        fields = ('id', 'title', 'todoitem_set')

class TodoListReadSerializer(serializers.ModelSerializer):
    todoitem_set = TodoItemSerializer(many=True,  read_only=True)
    created_by = serializers.StringRelatedField(source='created_by.username')

    class Meta:
        model = TodoList
        fields = ('id', 'title', 'todoitem_set', 'created_by')

class TodoItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'description', 'due_date', 'completed', 'todo_list_id')

class TodoItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'description', 'due_date', 'completed', 'todo_list_id')