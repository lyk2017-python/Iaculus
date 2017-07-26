from django.conf.urls import url
from forum.views import HomepageView, TopicView, PostView

urlpatterns = [
    url(r'^$', HomepageView),
    url(r'^topic/(?P<id>\d+)-(?P<slug>[A-za-z0-9\-]+)$', TopicView),
    url(r'^post/(?P<id>\d+)-(?P<slug>[A-za-z0-9\-]+)$', PostView)
]