from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import F, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from forum.forms import CategoriedTopicForm, ContactForm, NewPostForm, \
    TopicForm, CustomUserCreationForm
from forum.models import Category, Topic, Post

class LoginCreateView(LoginRequiredMixin, generic.CreateView):
    pass

class HomepageView(generic.ListView):
    """
    Anasayfada view: katogoriler ve spn gönderiler gösterilir
    """
    model = Category

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex["last_posts"] = Post.objects.all()
        contex["liked_posts"] = Post.objects.order_by("-score")
        contex["most_viewed_topics"] = Topic.objects.order_by("-viewed")
        return contex

class CategoryView(generic.FormView):
    """
    Kategori altındaki topicler sıralanır ve kategorisiz topic açılır
    """
    form_class = CategoriedTopicForm
    template_name = "forum/category_create.html"
    success_url = "."

    def get_success_url(self):
        return reverse("topic", kwargs={"slug" : self.object.slug})

    def get_category(self):
        query = Category.objects.filter(slug=self.kwargs["slug"])
        if query.exists():
            return query.get()
        else:
            raise Http404("Category not found")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["category"] = self.get_category().id
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self\
            .get_category()\
            .topics\
            .all()\
            .annotate(postcount=Count("posts"))\
            .order_by(self.get_ordering())
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_ordering(self):
        return self.request.GET.get("order", "id")

class TopicView(generic.CreateView):
    """
    Bir topic altındaki postlar sıralanır ve topic seçmeden post atılır
    """
    form_class = NewPostForm
    template_name = "forum/topic_create.html"
    success_url = "."

    @method_decorator(login_required)
    def post(self, request, *a, **kw):
        return super().post(request, *a, **kw)

    def get_topic(self):
        query = Topic.objects.filter(slug=self.kwargs["slug"]).order_by("created")
        if query.exists():
            return query.get()
        else:
            raise Http404("Topic not found")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["topic"] = self.get_topic().id
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_topic()
        object.viewed = F("viewed") + 1
        object.save(update_fields=["viewed"])
        object.refresh_from_db()
        context["object"] = object
        context["object_filter"] = object.posts.filter(hidden=False)
        return context

def like(request):
    id = request.POST.get("id", default=None)
    like = request.POST.get("like")
    obj = get_object_or_404(Post, id=int(id))
    if like == "true":
        obj.score = F("score") + 1
        obj.save(update_fields=["score"])
    elif like == "false":
        obj.score = F("score") - 1
        obj.save(update_fields=["score"])
    else:
        return HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"like": obj.score, "id": id})

def report(request):
    id = request.POST.get("id", default=None)
    report = request.POST.get("report")
    obj = get_object_or_404(Post, id=int(id))
    if report == "true":
        obj.report_count = F("report_count") + 1
        obj.save(update_fields=["report_count"])
    else:
        return HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"report": obj.report_count, "id": id})

class ContactFormView(generic.FormView):
    """
    Contact form page
    """
    form_class = ContactForm
    template_name = "forum/contact.html"
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        from django.conf import settings
        send_mail(
            "Iaculus ContactForm : {}".format(data["title"]),
            ("Sistemden size gelen bir bildirim var\n"
             "---\n"
             "{}\n"
             "---\n"
             "eposta={}\n"
             "ip={}").format(data["body"], data["email"],
                             self.request.META["REMOTE_ADDR"]),
            settings.DEFAULT_FROM_EMAIL,
            ["safafaydali@gmail.com"]
        )
        return super().form_valid(form)

class TopicCreateView(generic.FormView):
    """
    Anasayfadaki new post ile açılan sayfanın modeli: Kategorili topic açma
    """
    form_class = TopicForm
    template_name = "forum/topic_form.html"
    success_url = "."

    def get_success_url(self):
        return reverse("topic", kwargs={"slug" : self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

'''
ilerde sss eklemek istersek bunu kullanıcaz

class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"
'''

class RegistrationView(generic.FormView):
    form_class = CustomUserCreationForm
    template_name = "forum/signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
