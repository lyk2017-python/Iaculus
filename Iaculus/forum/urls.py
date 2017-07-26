from django.conf.urls import url
from forum.views import HomepageView, CategoryView, TopicView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="home"),
    url(r'^category/(?P<pk>\d+)$', CategoryView.as_view(), name="category"),
    url(r'^topic/(?P<pk>\d+)$', TopicView.as_view(), name="topic"),
    #url(r'^sss$', SSSView.as_view(), name="faq"),
]