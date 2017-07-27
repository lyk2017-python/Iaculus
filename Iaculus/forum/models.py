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


"""
from django.db import models

class Category(models.Model):
    """
    Category model; includes title, description and created time.Also
    update time is updated when new topic open under this category.
    """
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#{id} {title}".format(id=self.id, title=self.title)

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
    slug = models.SlugField()

    def __str__(self):
        return "#{id} {title}".format(id=self.id, title=self.title)

class Post(models.Model):
    """
    Post model; includes body, create time, updated time and related
    topic.Users can like posts.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, related_name="posts")
    body = models.TextField()
    like = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField()

    def __str__(self):
        return "#{id}".format(id=self.id)