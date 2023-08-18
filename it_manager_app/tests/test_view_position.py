from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from it_manager_app.models import Position

POSITION_FORMATS_URL = reverse("it_manager_app:position-list")
POSITION_CREATE_URL = reverse("it_manager_app:position-create")


class PublicPositionTests(TestCase):
    def test_login_requirement_list_position(self):
        res_list = self.client.get(POSITION_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login_requirement_create_position(self):
        res_create = self.client.get(POSITION_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_without_login_position(self):
        position = Position.objects.create(
            name="CEO"
        )
        url_1 = reverse(
            "it_manager_app:position-update", kwargs={"pk": position.pk}
        )
        url_2 = reverse(
            "it_manager_app:task-type-delete", kwargs={"pk": position.pk}
        )
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivatePositionFormatTests(TestCase):

    def setUp(self) -> None:
        number_position = 11

        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        for task_type_id in range(number_position):
            Position.objects.create(
                name=f"Bugs{task_type_id}",
            )

    def test_retrieve_position(self):
        response = self.client.get(POSITION_FORMATS_URL + "?page=1")
        response_2 = self.client.get(POSITION_FORMATS_URL + "?page=2")
        position = Position.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["position_list"])
             + list(response_2.context["position_list"])
             )
            , list(position)
        )
        self.assertTemplateUsed(response, "it_manager_app/position_list.html")

    def test_if_search_name_is_a_character_o1(self):
        response = self.client.get(POSITION_FORMATS_URL + "?name=O1")
        position = Position.objects.filter(
            name__icontains="O1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["position_list"]), list(position)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "O1")

    def test_view_url_exists_at_desired_location_position(self):
        response = self.client.get("/position/")
        self.assertEquals(response.status_code, 200)

    def test_pagination_is_ten_in_position_position(self):
        response = self.client.get(POSITION_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["position_list"]), 10)

    def test_pagination_is_second_position_page_one(self):
        response = self.client.get(POSITION_FORMATS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["position_list"]), 1)

    def test_create_success_url_position_is_with_redict_to_list(self):
        response = self.client.get(POSITION_CREATE_URL)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            POSITION_CREATE_URL, {"name": "test"}
        )
        self.assertRedirects(response, reverse("it_manager_app:position-list"))

    def test_update_success_url_position_is_with_redict_to_list(self):
        response = reverse("it_manager_app:position-update", kwargs={"pk": 1})

        response = self.client.post(
            response, {"name": "Test"}
        )
        position = Position.objects.get(id=1)
        self.assertEquals(str(position), "Test")
        self.assertRedirects(response, reverse("it_manager_app:position-list"))
