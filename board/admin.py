from django.contrib import admin
from .models import Community, News, Column, Notice


@admin.register(Community)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "name",
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


@admin.register(Column)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "date",
        "view",
    )


@admin.register(Notice)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
    )
