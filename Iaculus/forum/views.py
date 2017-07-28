from django.core.mail import send_mail
from django.http import Http404
from django.views import generic

from forum.forms import CategoriedTopicForm, ContactForm
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
        contex["posts"]=Post.objects.all()
        return contex

class TopicCreateView(generic.CreateView):
    model = Topic
    success_url = "/"
    fields = [
        "title",
        "category",
        "slug",
    ]

class CategoryView(generic.CreateView):
    """
    Kategori altındaki topicler sıralanıcak bu yüzden DetailView
    kullandık.Kategori detayları gösteriliyor yani.
    """
    form_class = CategoriedTopicForm
    template_name = "forum/category_create.html"
    success_url = "."

    def get_category(self):
        query = Category.objects.filter(pk=self.kwargs["pk"])
        if query.exists():
            return query.get()
        else:
            raise Http404("Category not found")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["category"] = [self.get_category()]
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_category()
        return context


class TopicView(generic.DetailView):
    """
    Kategoriyle aynı mantık.Bir topic altındaki postlar sıralanıcak
    """
    model = Topic

class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "forum/contact.html"

    def form_valid(self, form):
        data = form.cleaned_data
        from django.conf import settings
        send_mail(
            "Forum ContactForm : {}".format(data["title"]),
            ("Sistemden size gelen bir bildirim var\n"
             "---\n"
             "{}\n"
             "---\n"
             "eposta={}\n"
             "ip={}").format(data["body"], data["email"],
                             self.request.META["REMOTE_ADDR"],
                             settings.DEFAULT_FROM_EMAIL,
                             ["admin@iaculus.com"])
        )

'''
ilerde sss eklemek istersek bunu kullanıcaz

class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"
'''