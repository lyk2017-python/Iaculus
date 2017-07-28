from django.conf.urls import url
from forum.views import HomepageView, CategoryView, TopicView, ContactFormView, \
    TopicCreateView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="home"),
    url(r'^category/(?P<pk>\d+)/$', CategoryView.as_view(), name="category"),
    url(r'^newtopic/$', TopicCreateView.as_view(), name="newtopic"),
    url(r'^topic/(?P<pk>\d+)/$', TopicView.as_view(), name="topic"),
    url(r'^contact/$', ContactFormView.as_view(), name="contact"),
    #url(r'^sss$', SSSView.as_view(), name="faq"),
]