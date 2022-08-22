from django.db import models
from datetime import timedelta
from django.utils import timezone
from user.models import User

name_choice = (("자유", "자유"), ("정보", "정보"))


class Community(models.Model):
    title = models.CharField(max_length=64, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    name = models.CharField(max_length=32, choices=name_choice, verbose_name="분류")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like = models.PositiveIntegerField(default=0, verbose_name="추천수")
    like_users = models.ManyToManyField(User, related_name="like_boards", blank=True)

    @property
    def date_str(self):
        time = timezone.now() - self.date
        if time < timedelta(days=1):
            return self.date.strftime("%H:%M")
        else:
            return self.date.strftime("%m-%d")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Community"
        verbose_name = "커뮤니티"
        verbose_name_plural = "커뮤니티"


class Comment(models.Model):
    community = models.ForeignKey(
        Community, null=True, blank=True, on_delete=models.CASCADE, verbose_name="게시글"
    )
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="작성자"
    )
    content = models.CharField(max_length=2000, verbose_name="댓글 내용")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    @property
    def date_str(self):
        time = timezone.now() - self.date
        if time < timedelta(days=1):
            return self.date.strftime("%H:%M")
        else:
            return self.date.strftime("%m-%d")
