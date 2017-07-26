from django.conf.urls import url
from forum.views import HomepageView, TopicView, PostView, SSSView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="home"),
    url(r'^topic/(?P<id>\d+)-(?P<slug>[A-za-z0-9\-]+)$', TopicView.as_view(), name="topic"),
    url(r'^post/(?P<id>\d+)-(?P<slug>[A-za-z0-9\-]+)$', PostView.as_view(), name="post"),
    url(r'^sss$', SSSView.as_view(), name="faq"),
]