from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import HiddenInput
from django.http import HttpResponseRedirect

from forum.models import Topic, Post, Category, User


class NewPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":4}))
    class Meta:
        model = Post
        exclude = [
            "id",
            "score",
            "report_count",
            "hidden",
            "created",
            "updated",
        ]
        widgets = {
            "topic" : HiddenInput(),
            "slug" : HiddenInput(),
            "user" : HiddenInput(),
        }

class TopicForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects.all())
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))
    user = forms.ModelChoiceField(User.objects.filter(),
                                  widget=HiddenInput())

    def save(self):
        with transaction.atomic():
            topic = Topic.objects.create(title=self.cleaned_data["title"],
                                         category=self.cleaned_data["category"])
            Post.objects.create(topic=topic, body=self.cleaned_data["body"],user=self.cleaned_data["user"])
        return topic

class CategoriedTopicForm(forms.Form):
    title = forms.CharField()
    category = forms.ModelChoiceField(Category.objects.filter(),
                                      widget=HiddenInput())
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    user = forms.ModelChoiceField(User.objects.filter(),
                                      widget=HiddenInput())

    def save(self):
        with transaction.atomic():
            topic = Topic.objects.create(title=self.cleaned_data["title"],
                                         category=self.cleaned_data["category"])
            Post.objects.create(topic=topic, body=self.cleaned_data["body"],
                                user=self.cleaned_data["user"])
        return topic

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField(max_length=160)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
