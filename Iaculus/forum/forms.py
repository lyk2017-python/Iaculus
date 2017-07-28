from django import forms
from django.forms import HiddenInput

from forum.models import Topic


class CategoriedTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = [
            "id",
        ]
        widgets = {
            "categories" : HiddenInput()
        }
