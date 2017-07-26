from django.shortcuts import render
from django.views import generic
from forum.models import Category, Topic, Post


class HomepageView(generic.ListView):
    """
    Anasayfada kategoriler solda, son postlar sağda listelenicek.Bu yüzden
    ListView kullandıkŞu anda kategoriler listeleniyor ve ilgili kategori
    altındaki topiclere gidiyor, fakat postları sıralama yazılacak.
    """
    model = Category

    def get_context_data(self, **kwargs):
        """
        Bu method şu anda kategorileri sıralıyor fakat postları sıralıcak
        şekilde düzenlicez
        :param kwargs:
        :return:
        """
        contex = super().get_context_data(**kwargs)
        contex["topics"]=Topic.objects.all()
        return contex

class CategoryView(generic.DetailView):
    """
    Kategori altındaki topicler sıralanıcak bu yüzden DetailView
    kullandık.Kategori detayları gösteriliyor yani.
    """
    model = Category

class TopicView(generic.DetailView):
    """
    Kategoriyle aynı mantık.Bir topic altındaki postlar sıralanıcak
    """
    model = Topic


'''
ilerde sss eklemek istersek bunu kullanıcaz

class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"
'''