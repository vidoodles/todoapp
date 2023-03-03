from django.urls import path
from .views import (
    TodoListCreateView,   
    TodoListView,
    TodoListDetailView,
    TodoItemCreateView,
    TodoItemListView,
    TodoItemDetailView,
    TodoItemView,
    todo_list,
    login_view,
    todo_create,
    todo_edit,
    todo_delete,
    todo_item_create,
    todo_item_edit,
    todo_item_delete,
    logout_view
)
from django.conf.urls.static import static
from django.conf import settings

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
    path('todo/', todo_list, name='my-list'),
    path('todo/create/', todo_create, name='create'),
    path('todo/<uuid:list_id>/edit/', todo_edit, name='todo_edit'),
    path('todo/<uuid:list_id>/delete/', todo_delete, name='todo_delete'),
    path('todo/<uuid:list_id>/item_create/', todo_item_create, name='todo_item_create'),
    path('todoitem/<uuid:item_id>/edit/', todo_item_edit, name='todo_item_edit'),
    path('todoitem/<uuid:item_id>/delete/', todo_item_delete, name='todo_item_delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
