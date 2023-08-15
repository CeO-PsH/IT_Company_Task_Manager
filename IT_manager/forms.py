from django import forms

from it_manager_app.models import Task


class TacksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"