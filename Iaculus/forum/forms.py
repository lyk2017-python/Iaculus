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
            "category" : HiddenInput(),
            "closed" : HiddenInput(),
        }

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField(max_length=160)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))