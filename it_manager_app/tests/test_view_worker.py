from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from it_manager_app.models import TaskType, Worker, Task, Position

WORKER_FORMATS_URL = reverse("it_manager_app:worker-list")
WORKER_CREATE_URL = reverse("it_manager_app:worker-create")


class PublicWorkerFormatTests(TestCase):
    def test_login_requirement_list_worker(self):
        res_list = self.client.get(WORKER_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login__worker_requirement_create(self):
        res_create = self.client.get(WORKER_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_worker_without_login(self):
        username = "admin.user"
        password = "qwe12345"
        worker = Worker.objects.create_user(
            username=username,
            password=password,
        )

        url_1 = reverse("it_manager_app:worker-update", kwargs={"pk": worker.pk})
        url_2 = reverse("it_manager_app:worker-delete", kwargs={"pk": worker.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateWorkerTests(TestCase):

    def setUp(self) -> None:
        number_of_workers = 11
        position = Position.objects.create(
            name="CEO",
        )

        username = "user"
        password = "qwe12345"
        position = position

        self.user = get_user_model().objects.create_user(
            username="admin.user_test",
            password="vbn12345"
        )
        self.client.force_login(self.user)

        for worker_id in range(number_of_workers):
            Worker.objects.create_user(
                username=f"{username}{worker_id}",
                password=password,
                position=position
            )

    def test_retrieve_worker(self):
        response = self.client.get(WORKER_FORMATS_URL + "?page=1")
        response_2 = self.client.get(WORKER_FORMATS_URL + "?page=2")
        driver = Worker.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["worker_list"])
             + list(response_2.context["worker_list"])
             )
            , list(driver)
        )
        self.assertTemplateUsed(response, "it_manager_app/worker_list.html")

    def test_update_delete_worker_with_login(self):
        worker = Worker.objects.first()
        url_1 = reverse("it_manager_app:worker-update", kwargs={"pk": worker.pk})
        url_2 = reverse("it_manager_app:worker-delete", kwargs={"pk": worker.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)

    def test_if_search_name_is_admin_user(self):
        response = self.client.get(
            WORKER_FORMATS_URL + "?username=admin.user1"
        )
        worker = Worker.objects.filter(
            username__icontains="admin.user1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["worker_list"]), list(worker)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "admin.user1"
        )

    def test_view_url_exists_at_desired_location_worker(self):
        response = self.client.get("/worker/")
        self.assertEquals(response.status_code, 200)

    def test_pagination_in_worker_is_ten(self):
        response = self.client.get(WORKER_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["worker_list"]), 10)

    def test_pagination_is_second_worker_page_two(self):
        response = self.client.get(WORKER_FORMATS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["worker_list"]), 2)

    def test_create_worker_success_url_is_with_redict_to_list(self):
        position = Position.objects.create(
            name="Manager",
        )
        data_form = {
            "username": "ira@psh.com",
            "first_name": "Test1",
            "last_name": "Test2",
            "password1": "wG-k9qwNyfpDtwm",
            "password2": "wG-k9qwNyfpDtwm",
            "position": position.id
        }
        self.client.post(WORKER_CREATE_URL, data=data_form)
        new_user = get_user_model().objects.get(username=data_form["username"])
        self.assertEquals(new_user.first_name, data_form["first_name"])
        self.assertEquals(new_user.last_name, data_form["last_name"])
        self.assertEquals(new_user.position.id, data_form["position"])

    def test_update_worker_success_url_is_with_redict_to_list(self):
        response = reverse("it_manager_app:worker-update", kwargs={"pk": 3})
        data = {
            "first_name": "Test",
            "last_name": "Test2"
        }
        self.client.post(response, data)
        worker = Worker.objects.get(id=3)
        self.assertEquals(
            str(worker),
            f"Username: {worker.username}.({worker.first_name} {worker.last_name})"
        )
