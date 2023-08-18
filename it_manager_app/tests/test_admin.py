from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from it_manager_app.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        position = Position.objects.create(
            name="CEO",
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="user_test",
            password="qwe12345",
            position=position
        )

    def test_worker_position_listed(self):
        """Tests that worker`s position is on worker admin display"""
        url = reverse("admin:it_manager_app_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        """Tests that worker`s position is on worker admin page"""
        url = reverse("admin:it_manager_app_worker_change", args=[self.worker.id])
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)

    def test_worker_detail_add_information(self):
        """Tests that worker`s add information is on worker create page"""
        url = reverse("admin:it_manager_app_worker_add")
        res = self.client.get(url)

        self.assertContains(res, '<input type="text" name="first_name"')
        self.assertContains(res, '<input type="text" name="last_name"')
        self.assertContains(res, '<select name="position"')

    def test_search_fields_on_the_display(self):
        """Test check is search panel on the task display"""

        url = reverse("admin:it_manager_app_task_changelist")
        res = self.client.get(url)

        self.assertContains(res, '<input type="search"')
