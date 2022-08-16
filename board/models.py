from django.db import models
from datetime import timedelta
from django.utils import timezone
from user.models import User


class Community(models.Model):
    title = models.CharField(max_length=64, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    name = models.CharField(max_length=32, verbose_name="분류")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like = models.PositiveIntegerField(default=0, verbose_name="추천수")

    @property
    def date_str(self):
        time = timezone.now() - self.date
        if time < timedelta(days=1):
            return self.date.strftime("%-H:%-M")
        else:
            return self.date.strftime("%m-%d")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Community"
        verbose_name = "커뮤니티"
        verbose_name_plural = "커뮤니티"
