from django.conf.urls import url
from forum.views import like, HomepageView, CategoryView, TopicView, \
    ContactFormView, \
    TopicCreateView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="home"),
    url(r'^category/(?P<slug>[\w-]+)/$',
        CategoryView.as_view(), name="category"),
    url(r'^topic/(?P<slug>[\w-]+)/$', TopicView.as_view(), name="topic"),
    url(r'^newtopic/$', TopicCreateView.as_view(), name="newtopic"),
    url(r'^contact/$', ContactFormView.as_view(), name="contact"),
    url(r"^api/like$", like, name="like_dislike"),
    #url(r'^sss$', SSSView.as_view(), name="faq"),
]