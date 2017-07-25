from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#{id} {title}".format(id=self.id, title=self.title)

class Topic(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return "#{id} {title}".format(id=self.id, title=self.title)

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic)
    body = models.TextField()

    def __str__(self):
        return "#{id}".format(id=self.id)