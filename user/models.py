from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class User(AbstractUser):
    nickname = models.CharField(max_length=8, unique=True, verbose_name="닉네임")
    image = models.ImageField(
        default="profile_images/default.jpg",
        upload_to="profile_images/%Y-%m-%d/",
        verbose_name="프로필 이미지",
    )
    n_changed = models.DateTimeField(null=True, verbose_name="닉네임 변경일")
    exp = models.PositiveIntegerField(default=0)
    lv = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False, verbose_name="인증")
    social = models.BooleanField(default=False, verbose_name="소셜 계정")

    @property
    def nchanged(self):
        if self.n_changed == None:
            return True
        elif datetime.now() - timedelta(days=30) > self.n_changed:
            return False
        else:
            return True

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = "User"
        verbose_name = "유저"
        verbose_name_plural = "유저"
