from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from it_manager_app.models import TaskType

TASK_TYPE_FORMATS_URL = reverse("it_manager_app:task_type-list")
TASK_TYPE_CREATE_URL = reverse("it_manager_app:task-type-create")


class PublicTaskTypeFormatTests(TestCase):
    def test_login_requirement_list_task_type(self):
        res_list = self.client.get(TASK_TYPE_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login_requirement_create_task_type(self):
        res_create = self.client.get(TASK_TYPE_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_without_login_task_type(self):
        task_type = TaskType.objects.create(
            name="bugs"
        )
        url_1 = reverse(
            "it_manager_app:task-type-update", kwargs={"pk": task_type.pk}
        )
        url_2 = reverse(
            "it_manager_app:task-type-delete", kwargs={"pk": task_type.pk}
        )
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateTaskTypeFormatTests(TestCase):

    def setUp(self) -> None:
        number_task_type = 11

        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        for task_type_id in range(number_task_type):
            TaskType.objects.create(
                name=f"Bugs{task_type_id}",
            )

    def test_retrieve_task_type(self):
        response = self.client.get(TASK_TYPE_FORMATS_URL + "?page=1")
        response_2 = self.client.get(TASK_TYPE_FORMATS_URL + "?page=2")
        task_type = TaskType.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["task_type_list"])
             + list(response_2.context["task_type_list"])
             )
            , list(task_type)
        )
        self.assertTemplateUsed(response, "it_manager_app/task_type_list.html")

    def test_update_delete_type_task_wit_login(self):
        task_type = TaskType.objects.first()
        url_1 = reverse(
            "it_manager_app:task-type-update", kwargs={"pk": task_type.pk}
        )
        url_2 = reverse(
            "it_manager_app:task-type-delete", kwargs={"pk": task_type.pk}
        )
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)

    def test_if_search_name_is_a_character_s1(self):
        response = self.client.get(TASK_TYPE_FORMATS_URL + "?name=s1")
        task_type = TaskType.objects.filter(
            name__icontains="s1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["task_type_list"]), list(task_type)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "s1")

    def test_view_url_exists_at_desired_location_task_type(self):
        response = self.client.get("/task_type/")
        self.assertEquals(response.status_code, 200)

    def test_pagination_is_five_task_type(self):
        response = self.client.get(TASK_TYPE_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["task_type_list"]), 10)

    def test_pagination_is_second_page_five(self):
        response = self.client.get(TASK_TYPE_FORMATS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["task_type_list"]), 1)

    def test_create_success_url_is_with_redict_to_list(self):
        response = self.client.get(TASK_TYPE_CREATE_URL)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            TASK_TYPE_CREATE_URL, {"name": "test"}
        )
        self.assertRedirects(response, reverse("it_manager_app:task_type-list"))

    def test_update_success_url_is_with_redict_to_list(self):
        response = reverse("it_manager_app:task-type-update", kwargs={"pk": 1})

        response = self.client.post(
            response, {"name": "Test"}
        )
        task_type = TaskType.objects.get(id=1)
        self.assertEquals(str(task_type), "Test")
        self.assertRedirects(response, reverse("it_manager_app:task_type-list"))
