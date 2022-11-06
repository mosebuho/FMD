from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "userid",
        "image",
        "name",
        "email",
        "join_date",
        "last_login",
    )
