from django.conf.urls import url
from forum.views import HomepageView, TopicView, PostView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="home"),
    url(r'^topic/(?P<pk>\d+)$', TopicView.as_view(), name="topic"),
    url(r'^post/(?P<pk>\d+)$', PostView.as_view(), name="post"),
    #url(r'^sss$', SSSView.as_view(), name="faq"),
]