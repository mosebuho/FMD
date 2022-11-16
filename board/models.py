from django.db import models
from datetime import datetime
from user.models import User


class Community(models.Model):
    title = models.CharField(max_length=64, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like = models.PositiveIntegerField(default=0, verbose_name="추천수")
    like_users = models.ManyToManyField(User, related_name="like_boards", blank=True)

    @property
    def date_short(self):
        time = self.date.strftime("%Y%m%d")
        today = datetime.now().strftime("%Y%m%d")
        if time == today:
            return self.date.strftime("%H:%M")
        else:
            return self.date.strftime("%m-%d")

    @property
    def date_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M")

    @property
    def view_count(self):
        self.view += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Community"
        verbose_name = "커뮤니티"
        verbose_name_plural = "커뮤니티"
        ordering = ["-date"]


class Comment(models.Model):
    community = models.ForeignKey(
        Community, null=True, blank=True, on_delete=models.CASCADE, verbose_name="게시글"
    )
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="작성자"
    )
    content = models.CharField(max_length=2000, verbose_name="댓글 내용")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    @property
    def date_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M")

    class Meta:
        ordering = ["-date"]


class News(models.Model):
    title = models.CharField(max_length=128, verbose_name="제목")
    thumbnail = models.ImageField(
        null=False,
        blank=False,
        upload_to="news_thumbnial/%Y-%m-%d/",
        verbose_name="썸네일",
    )
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")

    @property
    def date_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M")

    @property
    def view_count(self):
        self.view += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "News"
        verbose_name = "뉴스"
        verbose_name_plural = "뉴스"
        ordering = ["-date"]


class Column(models.Model):
    title = models.CharField(max_length=128, verbose_name="제목")
    thumbnail = models.ImageField(
        null=False,
        blank=False,
        upload_to="column_thumbnial/%Y-%m-%d/",
        verbose_name="썸네일",
    )
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")

    @property
    def date_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M")

    @property
    def view_count(self):
        self.view += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Column"
        verbose_name = "칼럼"
        verbose_name_plural = "칼럼"
        ordering = ["-date"]


class Notice(models.Model):
    title = models.CharField(max_length=128, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    @property
    def date_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Notice"
        verbose_name = "공지"
        verbose_name_plural = "공지"
        ordering = ["-date"]


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="제목")
    thumbnail = models.ImageField(
        null=False,
        blank=False,
        upload_to="event_thumbnial/%Y-%m-%d/",
        verbose_name="썸네일",
    )
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    start = models.DateTimeField(null=True, blank=True, verbose_name="시작")
    end = models.DateTimeField(null=True, blank=True, verbose_name="종료")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Event"
        verbose_name = "행사"
        verbose_name_plural = "행사"


class Image(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="summernote/%Y-%m-%d/")
