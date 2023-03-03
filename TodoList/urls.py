from django.urls import path
from .views import (
    TodoListCreateView,   
    TodoListView,
    TodoListDetailView,
    TodoItemCreateView,
    TodoItemListView,
    TodoItemDetailView,
    TodoItemView
)

urlpatterns = [
    path('todolist/', TodoListView.as_view(), name='list-lists'),
    path('todolist/create/', TodoListCreateView.as_view(), name='create-list'),
    path('todolist/<uuid:pk>/', TodoListDetailView.as_view(), name='detail-list'),
    path('todolist/<uuid:todo_list_id>/items/create/',
         TodoItemCreateView.as_view(), name='create-item'),
    path('todolist/<uuid:todo_list_id>/items/',
         TodoItemListView.as_view(), name='list-items'),
    path('todoitems/', TodoItemView.as_view(), name='list-all-items'),
    path('todoitems/create/', TodoItemCreateView.as_view(), name='create-item'),
    path('todoitems/<uuid:pk>/',
         TodoItemDetailView.as_view(), name='detail-item'),
]
