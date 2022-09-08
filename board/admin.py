from django.contrib import admin
from .models import Community, News


@admin.register(Community)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "name",
        "content",
        "writer",
        "date",
        "view",
        "like",
    )


@admin.register(News)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "name",
        "writer",
        "date",
        "view",
    )
