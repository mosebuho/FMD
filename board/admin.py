from django.contrib import admin
from .models import Community, News, Column, Notice, Event


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "date",
        "view",
        "like",
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "date",
        "view",
    )


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "date",
        "view",
    )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start",
        "end",
    )
