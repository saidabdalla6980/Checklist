

from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),  # Example view
    path('create/', views.task_create, name='task-create'),  # Task creation
    path('<int:pk>/detail/', views.task_detail, name='task-detail'),  # Task details
    path('<int:pk>/update/', views.task_update, name='task-update'),  # Task update
    path('<int:pk>/delete/', views.task_confirm_delete, name='task-delete'),  # Task delete
]
