from django.contrib.auth.models import AbstractUser

app_name = "user"


class User(AbstractUser):
    pass

    class Meta:
        db_table = "User"
        verbose_name = "유저"
        verbose_name_plural = "유저"
