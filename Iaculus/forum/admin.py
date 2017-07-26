from django.contrib import admin
from forum.models import Post, Topic, Category

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)