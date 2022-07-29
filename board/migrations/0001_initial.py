# Generated by Django 4.0.6 on 2022-07-29 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='글 제목')),
                ('content', models.TextField(verbose_name='글 내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('board_name', models.CharField(max_length=32, verbose_name='게시판 종류')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '게시판',
                'verbose_name_plural': '게시판',
                'db_table': 'board',
            },
        ),
    ]
