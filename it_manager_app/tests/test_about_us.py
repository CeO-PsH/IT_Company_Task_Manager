from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

ABOUT_US_FORMATS_URL = reverse("it_manager_app:about-us")


class PublicAboutUsTests(TestCase):
    def test_login_requirement_abou_us(self):
        res_list = self.client.get(ABOUT_US_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)


class PrivateIndexFormatTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_about_us(self):

        response = self.client.get(ABOUT_US_FORMATS_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "it_manager_app/about-us.html")
