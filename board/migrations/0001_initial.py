# Generated by Django 4.0.6 on 2022-09-14 08:11

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
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('thumbnail', models.ImageField(upload_to='', verbose_name='썸네일')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('name', models.CharField(choices=[('국내', '국내'), ('해외', '해외')], max_length=32, verbose_name='분류')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '뉴스',
                'verbose_name_plural': '뉴스',
                'db_table': 'News',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('name', models.CharField(choices=[('자유', '자유'), ('정보', '정보')], max_length=32, verbose_name='분류')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='추천수')),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_boards', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '커뮤니티',
                'verbose_name_plural': '커뮤니티',
                'db_table': 'Community',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000, verbose_name='댓글 내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.community', verbose_name='게시글')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('thumbnail', models.ImageField(upload_to='', verbose_name='썸네일')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '칼럼',
                'verbose_name_plural': '칼럼',
                'db_table': 'Column',
                'ordering': ['-date'],
            },
        ),
    ]
