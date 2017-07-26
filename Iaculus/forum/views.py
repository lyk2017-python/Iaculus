from django.shortcuts import render
from django.views import generic
from forum.models import Category, Topic, Post


class HomepageView(generic.ListView):
    model = Category

class TopicView(generic.ListView):
    model = Topic

class PostView(generic.DetailView):
    def get_queryset(self):
        return Post.objects.all()

class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"