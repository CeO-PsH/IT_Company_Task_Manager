from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from IT_manager.forms import TacksForm
from it_manager_app.models import Worker, Task, TaskType, Position


def index(request):
    num_worker = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_type_of_tasks = TaskType.objects.count()
    position = Position.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_worker" : num_worker,
        "num_tasks": num_tasks,
        "num_type_of_tasks": num_type_of_tasks,
        "position": position,
        "num_visits": num_visits
    }
    return render(request, "it_manager_app/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "it_manager_app/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("it_manager_app:task_type-list")
    template_name = "it_manager_app/task_type_form.html"



class TaskTypeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("it_manager_app:task_type-list")
    template_name = "it_manager_app/task_type_form.html"


class TaskTypeDelete(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("it_manager_app:task_type-list")
    template_name = "it_manager_app/task_type_delete_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")
    paginate_by = 10


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TacksForm
    success_url = reverse_lazy("it_manager_app:position-list")
    template_name = "it_manager_app/task_form.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("it_manager_app:position-list")

class PositionTypeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("it_manager_app:position-list")

class PositionTypeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("it_manager_app:position-list")
    template_name = "it_manager_app/position_delete_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
