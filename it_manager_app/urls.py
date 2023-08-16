from django.urls import path
from it_manager_app.views import (
    index,
    TaskTypeListView,
    TaskListView,
    PositionListView,
    WorkerListView,
    TaskDetailView,
    WorkerDetailView,
    TaskCreateView,
    TaskTypeCreateView,
    PositionCreateView,
    TaskTypeDelete,
    TaskTypeUpdate,
    PositionTypeDelete,
    PositionTypeUpdate,
    WorkerCreateView,
    TaskUpdateView
)

urlpatterns = [
    path("", index, name = "index"),
    path("task_type/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task_type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task_type/<int:pk>/delete/", TaskTypeDelete.as_view(), name="task-type-delete"),
    path("task_type/<int:pk>/update/", TaskTypeUpdate.as_view(), name="task-type-update"),
    path("task/", TaskListView.as_view(), name="tasks-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name = "task-detail"),
    path("task/create/", TaskCreateView.as_view(), name = "task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("position/", PositionListView.as_view(), name = "position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/delete/", PositionTypeDelete.as_view(), name="position-delete"),
    path("position/<int:pk>/update/", PositionTypeUpdate.as_view(), name="position-update"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name = "worker-detail")
]

app_name = "it_manager_app"
