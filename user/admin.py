from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(User, UserAdmin)
class UserAdmin(admin.ModelAdmin):
    UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", "image", "verified")}),)
    UserAdmin.list_display = (
        "username",
        "email",
        "nickname",
        "exp",
        "lv",
        "verified",
        "n_changed",
        "social",
    )
