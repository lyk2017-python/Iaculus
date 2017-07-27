from django.contrib import admin
from forum.models import Post, Topic, Category

"""
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
"""

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ # Listede gösterilecek kolonlar
        "title",
        "created",
        "updated"
    ]
    search_fields = [ # Arama yapılacak özellikler
        "title"
    ]
    list_filter = [ # Filtrelenecek özellikler
        "created",
        "updated"
    ]
    """
    fieldsets = [
        (
            "Global",
            {
                "fields": [
                    "title",
                ]
            }
        ),
    ]
    """

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = [  # Listede gösterilecek kolonlar
        "title",
        "category",
        "created",
        "updated",
        "closed",
    ]
    search_fields = [  # Arama yapılacak özellikler
        "title",
        "category__title",
    ]
    list_filter = [  # Filtrelenecek özellikler
        "created",
        "updated",
        "closed",
        "category",
    ]
    fieldsets = [
        (
            "Global",
            {
                "fields": [
                    ("title", "slug"),
                    ("category", "closed"),
                ]
            }
        ),
    ]

@admin.register(Post)
class TopicAdmin(admin.ModelAdmin):
    list_display = [  # Listede gösterilecek kolonlar
        "topic",
        "like",
        "created",
        "updated",
    ]
    search_fields = [  # Arama yapılacak özellikler
        "topic__title",
    ]
    list_filter = [  # Filtrelenecek özellikler
        "created",
        "updated",
        "like",
    ]
    fieldsets = [
        (
            "Global",
            {
                "fields": [
                    ("topic", "slug"),
                    "body",
                ]
            }
        ),
    ]