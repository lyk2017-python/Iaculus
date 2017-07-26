from django.shortcuts import render
from django.views import generic


class HomepageView(generic.ListView):
    model = Category

class TopicView(generic.ListView):


class PostView(generic.DetailView):
