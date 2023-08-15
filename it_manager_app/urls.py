from django.urls import path
from it_manager_app.views import index, TaskTypeListView, TaskListView, PositionListView, WorkerListView, \
    TaskDetailView, WorkerDetailView, TaskCreateView, TaskTypeCreateView, PositionCreateView

urlpatterns = [
    path("", index, name = "index"),
    path("task_type/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task_type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task/", TaskListView.as_view(), name="tasks-list"),
    path("task/int:<pk>/", TaskDetailView.as_view(), name = "task-detail"),
    path("task/create/", TaskCreateView.as_view(), name = "task-create"),
    path("position/", PositionListView.as_view(), name = "position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/int:<pk>/", WorkerDetailView.as_view(), name = "worker-detail")
]

app_name = "it_manager_app"
