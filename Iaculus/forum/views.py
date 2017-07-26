from django.shortcuts import render
from django.views import generic
from forum.models import Category, Topic, Post


class HomepageView(generic.ListView):
    model = Category

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex["topics"]=Topic.objects.all()
        return contex

class CategoryView(generic.DetailView):
    model = Category

class TopicView(generic.DetailView):
    model = Topic


'''
class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"
'''