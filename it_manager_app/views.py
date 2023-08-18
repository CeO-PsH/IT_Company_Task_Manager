from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from IT_manager.forms import (
    TacksForm,
    WorkerCreationForm,
    SearchForm,
    WorkersSearchForm
)
from it_manager_app.models import Worker, Task, TaskType, Position


@login_required
def index(request):
    num_worker = Worker.objects.count()
    num_tasks = Task.objects.filter(is_completed=True).count()
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = SearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()

        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


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
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = SearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")

        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TacksForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TacksForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("it_manager_app:task-list")
    template_name = "it_manager_app/task_delete_confirm_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = SearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Position.objects.all()

        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkersSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        queryset = Worker.objects.all()

        form = WorkersSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("it_manager_app:worker-list")
    template_name = "it_manager_app/worker_delete_confirm_delete.html"


@login_required
def task_assign(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in worker.tasks.all()
    ):  # probably could check if car exists
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("it_manager_app:task-detail", args=[pk])
    )


@login_required
def about_us(request):
    return render(request, "it_manager_app/about-us.html")
