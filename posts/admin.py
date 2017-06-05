from django.contrib import admin
from .models import Table, Post


admin.site.register(
    Table,
    list_display=["id", "title", "slug"],
    list_display_links=["id", "title"],
    ordering=["title"],
    prepopulated_fields={"slug": ("title",)},
)


admin.site.register(
    Post,
    list_display=["id", "tables", "created", "body_intro"],
    ordering=["-id"],
)
