from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from it_manager_app.models import TaskType, Task


TASK_URL = reverse("it_manager_app:task-list")
TASK_CREATE_URL = reverse("it_manager_app:task-create")


class PublicTaskTests(TestCase):
    @classmethod
    def setUp(cls) -> None:
        task_type = TaskType.objects.create(
            name="bugs",
        )
        Task.objects.create(
            name="bugs_test",
            description = "bugs test bugs",
            deadline = datetime.now(),
            is_completed = False,
            priority="low",
            task_type=task_type
        )

    def test_login_requirement_task(self):
        res_list = self.client.get(TASK_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login_requirement_task_creste(self):
        res_create = self.client.get(TASK_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)


    def test_update_delete_task_without_login(self):
        task = Task.objects.get(id=1)
        url_1 = reverse("it_manager_app:task-update", kwargs={"pk": task.pk})
        url_2 = reverse("it_manager_app:task-delete", kwargs={"pk": task.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateTaskTests(TestCase):

    def setUp(self) -> None:
        number_of_task = 11
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        task_type = TaskType.objects.create(
            name="bugs",
        )
        for car_id in range(number_of_task):
            Task.objects.create(
                name=f"bugs_test{car_id}",
                description="bugs test bugs",
                deadline=datetime.now(),
                is_completed=False,
                priority="low",
                task_type=task_type
            )

    def test_retrieve_task(self):
        response = self.client.get(TASK_URL + "?page=1")
        response_2 = self.client.get(TASK_URL + "?page=2")
        task = Task.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["task_list"])
             + list(response_2.context["task_list"])
             )
            , list(task)
        )
        self.assertTemplateUsed(response, "it_manager_app/task_list.html")

    def test_if_search_test_name_is_a_character_est3(self):
        response = self.client.get(TASK_URL + "?name=est3")
        task = Task.objects.filter(
            name__icontains="est3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["task_list"]), list(task)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "est3"
        )

    def test_view_url_task_exists_at_desired_location(self):
        response = self.client.get("/task/")
        self.assertEquals(response.status_code, 200)

    def test_pagination_in_task_is_ten(self):
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["task_list"]), 10)

    def test_pagination_in_task_is_second_page_1(self):
        response = self.client.get(TASK_URL + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_update_delete_task_with_login(self):
        task = Task.objects.first()
        url_1 = reverse("it_manager_app:task-update", kwargs={"pk": task.pk})
        url_2 = reverse("it_manager_app:task-delete", kwargs={"pk": task.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)

