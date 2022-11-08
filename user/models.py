from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class User(AbstractUser):
    nickname = models.CharField(max_length=8, unique=True, verbose_name="닉네임")
    image = models.ImageField(
        default="profile_images/default.png",
        upload_to="profile_images/%Y/%m/%d/",
        verbose_name="프로필 이미지",
    )
    n_changed = models.DateTimeField(auto_now_add=True, verbose_name="닉네임 변경일")

    @property
    def nchanged(self):
        return datetime.now() - timedelta(days=30) < self.n_changed

    def __str__(self):
        return self.username

    class Meta:
        db_table = "User"
        verbose_name = "유저"
        verbose_name_plural = "유저"
