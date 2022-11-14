from django.contrib import admin
from .models import Community, News, Column, Notice, Event
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Community)
class CommunityAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "writer",
        "date",
        "view",
        "like",
    )


@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "writer",
        "date",
        "view",
    )


@admin.register(Column)
class ColumnAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
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
class EventAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "start",
        "end",
    )
