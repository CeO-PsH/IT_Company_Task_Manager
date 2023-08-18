from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from IT_manager.forms import WorkerCreationForm, TacksForm
from it_manager_app.models import Worker, Position


class FormsTests(TestCase):

    def test_worker_creation_form_position_first_name_last_name(self):
        position = Position.objects.create(
            name="CEO"
        )
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test",
            "last_name": "last",
            "position": position
        }

        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertDictEqual(form.cleaned_data, form_data)

    def test_task_form_update_incorrect_date(self):
        current_date = datetime.today()
        date_2_days_ago = current_date - timedelta(days=2)
        form_data = {"deadline": date_2_days_ago }
        form = TacksForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_update_correct_date(self):
        current_date = datetime.today()
        form_data = {"deadline": current_date }
        form = TacksForm(data=form_data)
        self.assertFalse(form.is_valid())
