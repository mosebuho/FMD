from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, userid, email, name, password=None):
        if not userid:
            raise ValueError("아이디는 필수 항목입니다.")

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
        user.level = 3
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userid = models.CharField(max_length=60, unique=True, verbose_name="아이디")
    email = models.EmailField(max_length=128, unique=True, verbose_name="이메일")
    name = models.CharField(max_length=60, unique=True, verbose_name="닉네임")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="생성시간")
    point = models.PositiveIntegerField(default=0, verbose_name="포인트")
    level = models.PositiveIntegerField(default=0, verbose_name="레벨")
    image = models.ImageField(default='profile_images/default.png', upload_to='profile_images/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
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
