from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from it_manager_app.models import TaskType, Task, Position, Worker


@admin.register(Task)
class TaskModel(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type"
    ]
    list_filter = ["task_type"]
    search_fields = ["name"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Info about position", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info",
         {"fields": ("position", "first_name", "last_name")}
         ),
    )


admin.site.register(TaskType)
admin.site.register(Position)
