from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ("Urgent", "Very important")
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(auto_now_add=False)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name"
            )
        ]

    def __str__(self):
        return (
            f"Name: {self.name}, description: {self.description}."
            f" Priority: {self.priority}. Who assignees {self.assignees}."
            f" Completed: {self.is_completed}"
        )


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return self.name

class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers", null=True)

    class Meta:
        ordering = ["username"]


    def __str__(self):
        return f"Username: {self.username}.({self.first_name} {self.last_name})"
