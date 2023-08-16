from django.utils import timezone
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from django.utils.datetime_safe import datetime

from it_manager_app.models import Task, Worker



class TacksForm(forms.ModelForm):
    today = datetime.now()
    aware_datetime = timezone.make_aware(today, timezone.get_default_timezone())
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required=False
    )

    deadline = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        date_format='%d/%m/%Y',
        time_attrs={
            'type':'time'
            },
        time_format='%H:%M',
        ),
        validators=[MinValueValidator(aware_datetime)])


    class Meta:
        model = Task
        fields = "__all__"



class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("position","first_name", "last_name",)

class SearchForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TimeInput(attrs={"placeholder": "Search by name"})
    )


