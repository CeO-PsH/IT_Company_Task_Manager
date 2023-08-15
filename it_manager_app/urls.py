from django.urls import path
from it_manager_app.views import index, TaskTypeListView, TaskListView, PositionListView, WorkerListView, \
    TaskDetailView, WorkerDetailView

urlpatterns = [
    path("", index, name = "index"),
    path("task_type/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task/", TaskListView.as_view(), name="tasks-list"),
    path("task/int:<pk>/", TaskDetailView.as_view(), name = "task-detail"),
    path("position/", PositionListView.as_view(), name = "position-list"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/int:<pk>/", WorkerDetailView.as_view(), name = "worker-detail")
]

app_name = "it_manager_app"
