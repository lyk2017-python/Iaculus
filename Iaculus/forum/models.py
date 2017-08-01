"""
                             . .  ,  ,
                              |` \/ \/ \,',
                              ;          ` \/\,.
                             :               ` \,/
                             |                  /
                             ;                 :
                            :                  ;
                            |      ,---.      /
                           :     ,'     `,-._ \
                           ;    (   o    \   `'
                         _:      .      ,'  o ;
                        /,.`      `.__,'`-.__,
                        \_  _               \
                       ,'  / `,          `.,'
                 ___,'`-._ \_/ `,._        ;
              __;_,'      `-.`-'./ `--.____)
           ,-'           _,--\^-'
         ,:_____      ,-'     \
        (,'     `--.  \;-._    ;
        :    Y      `-/    `,  :
        :    :       :     /_;'
        :    :       |L    :
         \    \      :    :
          `-._ `-.__, \    `.
             \   \  `. \     `.
           ,-;    \   )_\ ,','/
           \_ `---'--'" ,'^-;'
           (_`     ---'" ,-')
           / `--.__,. ,-'    \
           )-.__,-- ||___,--' `-.
          /._______,|__________,'\
          `--.____,'|_________,-'

The Simpsons
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Category(models.Model):
    """
    Category model; includes title, description and created time.Also
    update time is updated when new topic open under this category.
    """
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return "{title}".format(title=self.title)

    class Meta:
        get_latest_by = "created"
        ordering = ["title"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Topic(models.Model):
    """
    Topic model; includes title, related category, created time and update
    time that updated when new post added this topic.If the topic is closed
    by moderators, users can not post message under this topic.
    """
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name="topics")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)
    viewed = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return "{title}".format(id=self.id, title=self.title)

class Post(models.Model):
    """
    Post model; includes body, create time, updated time and related
    topic.Users can like posts.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, related_name="posts")
    body = models.TextField()
    score = models.SmallIntegerField(default=0)
    report_count = models.PositiveSmallIntegerField(default=0)
    hidden = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return "#{id}".format(id=self.id)

    class Meta:
        get_latest_by = "-created"
        ordering = ["-created"]

class User(AbstractUser):
    biograpyh = models.TextField(max_length=300)

@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Topic)
@receiver(pre_save, sender=Post)
def slug_belirle(sender, instance, *args, **kwargs):
    if not instance.slug:
        if hasattr(sender, "title"):
            instance.slug = slugify(instance.title)
        elif hasattr(sender, "topic"):
            instance.slug = slugify(instance.topic)
        else:
            raise AttributeError("Slug belirlemek için title ya da topic girin.")
    return instance

@receiver(pre_save, sender=Post)
def auto_hidden(sender, instance, *args, **kwargs):
    if instance.report_count >= 10:
        instance.hidden = True
    return instance