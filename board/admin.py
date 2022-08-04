from django.contrib import admin
from .models import Community


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
