from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from it_manager_app.models import Worker, Task, TaskType, Position


def index(request):
    num_worker = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_type_of_tasks = TaskType.objects.count()
    position = Position.objects.count()

    context = {
        "num_worker" : num_worker,
        "num_tasks": num_tasks,
        "num_type_of_tasks": num_type_of_tasks,
        "position": position,
    }
    return render(request, "it_manager_app/index.html", context=context)


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "it_manager_app/task_type.html"
    context_object_name = "task_type_list"
    paginate_by = 10


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")
    paginate_by = 10


class TaskDetailView(generic.DetailView):
    model = Task


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 10


class WorkerDetailView(generic.DetailView):
    model = Worker
