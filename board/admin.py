from django.contrib import admin
from .models import Community, News, Column, Notice, Event
from django_summernote.admin import SummernoteModelAdmin


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
class NoticeAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "content",
        "writer",
        "date",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "start",
        "end",
    )
