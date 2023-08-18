from django.contrib.auth import get_user_model
from datetime import datetime
from django.test import TestCase
from it_manager_app.models import Task, TaskType, Position, Worker


class ModelsTest(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="bugs",
        )
        self.assertEqual(
            str(task_type),
            f"{task_type.name}"
        )

    def test_position_str(self):
        position = Position.objects.create(
            name="CEO",
        )
        self.assertEqual(
            str(position),
            f"{position.name}"
        )

    def test_worker_str(self):
        worker = get_user_model().objects.create(
            username="admin.user",
            password="qwe12345",
            first_name="Admin",
            last_name="last_admin"
        )

        self.assertEqual(
            str(worker),
            f"Username: {worker.username}.({worker.first_name} {worker.last_name})"
        )

    def test_create_worker_with_position(self):
        username = "admin.user"
        password = "qwe12345"
        position = Position.objects.create(
            name="CEO",
        )
        worker = Worker.objects.create_user(
            username=username,
            password=password,
            position=position
        )

        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)

    def test_task_str(self):
        task_type = TaskType.objects.create(
            name="bugs",
        )

        task = Task.objects.create(
            name="web",
            description="try reconnect web to basedata",
            deadline=datetime.now(),
            is_completed=False,
            priority="low",
            task_type=task_type,
        )

        self.assertEqual(str(task), (
            f"Name: {task.name}, description: {task.description}."
            f" Priority: {task.priority}.Completed: {task.is_completed}"
        ))
