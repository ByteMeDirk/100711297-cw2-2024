from django.urls import path

from .views import create_task, list_tasks, edit_task, delete_task, mark_task_complete, mark_task_incomplete

urlpatterns = [
    path("create_task/", create_task, name="create_task"),
    path("list_tasks/", list_tasks, name="list_tasks"),
    path("edit_task/<int:task_id>/", edit_task, name="edit_task"),
    path("delete_task/<int:task_id>/", delete_task, name="delete_task"),
    path("mark_task_complete/<int:task_id>/", mark_task_complete, name="mark_task_complete"),
    path("mark_task_incomplete/<int:task_id>/", mark_task_incomplete, name="mark_task_incomplete"),
]
