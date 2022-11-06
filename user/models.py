from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.password_validation import name_validate, id_validate


class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, userid, email, name, password=None):
        user = self.model(userid=userid, email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, email, name, password):
        user = self.create_user(
            userid=userid,
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userid = models.CharField(
        max_length=20, unique=True, validators=[id_validate], verbose_name="아이디"
    )
    email = models.EmailField(max_length=32, unique=True, verbose_name="이메일")
    name = models.CharField(
        max_length=8, unique=True, validators=[name_validate], verbose_name="닉네임"
    )
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    image = models.ImageField(
        default="profile_images/default.png", upload_to="profile_images/%Y/%m/%d/"
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "userid"
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "User"
        verbose_name = "유저"
        verbose_name_plural = "유저"
