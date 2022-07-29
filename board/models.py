from django.db import models
from datetime import datetime, timedelta, timezone


class Board(models.Model):
    title = models.CharField(max_length=64, verbose_name="글 제목")
    content = models.TextField(verbose_name="글 내용")
    writer = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, verbose_name="작성자"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    board_name = models.CharField(max_length=32, verbose_name="게시판 종류")
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.date
        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.date.date()
            return str(time.days) + "일 전"
        else:
            return self.date.strftime("%m/%d")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "board"
        verbose_name = "게시판"
        verbose_name_plural = "게시판"
