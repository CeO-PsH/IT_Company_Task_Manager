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
    TaskDeleteView,
    TaskTypeCreateView,
    PositionCreateView,
    TaskTypeDelete,
    TaskTypeUpdate,
    PositionTypeDelete,
    PositionTypeUpdate,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskUpdateView,
    task_assign,
    about_us
)

urlpatterns = [
    path("", index, name = "index"),
    path("task_type/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task_type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task_type/<int:pk>/delete/", TaskTypeDelete.as_view(), name="task-type-delete"),
    path("task_type/<int:pk>/update/", TaskTypeUpdate.as_view(), name="task-type-update"),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name = "task-detail"),
    path("task/create/", TaskCreateView.as_view(), name = "task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("position/", PositionListView.as_view(), name = "position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/delete/", PositionTypeDelete.as_view(), name="position-delete"),
    path("position/<int:pk>/update/", PositionTypeUpdate.as_view(), name="position-update"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name = "worker-detail"),
    path("worker/<int:pk>/update", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker-delete"),
    path("task_assign/<int:pk>/", task_assign, name="task-assign"),
    path("about_us/",about_us, name="about-us")
]

app_name = "it_manager_app"
