from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from it_manager_app.models import TaskType, Task, Worker, Position

INDEX_FORMATS_URL = reverse("it_manager_app:index")


class PublicIndexFormatTests(TestCase):
    def test_login_requirement_index(self):
        res_list = self.client.get(INDEX_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)


class PrivateIndexFormatTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        task_type = TaskType.objects.create(
            name="Bugs",
        )

        Task.objects.create(
            name="bugs_test",
            description="bugs test bugs",
            is_completed=False,
            priority="low",
            task_type=task_type
        )

        Position.objects.create(
            name="CEO",
        )

    def test_retrieve_index(self):

        response = self.client.get(INDEX_FORMATS_URL)
        num_worker = Worker.objects.count()
        num_tasks = Task.objects.count()
        num_type_of_tasks = TaskType.objects.count()
        nuw_position = Position.objects.count()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["num_worker"], num_worker)
        self.assertEquals(response.context["position"], nuw_position)
        self.assertEquals(
            response.context["num_type_of_tasks"],
            num_type_of_tasks
        )
        self.assertEquals(response.context["num_worker"], num_tasks)
        self.assertEquals(response.context["num_visits"], 1)
        self.assertTemplateUsed(response, "it_manager_app/index.html")

    def test_view_url_index_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEquals(response.status_code, 200)


