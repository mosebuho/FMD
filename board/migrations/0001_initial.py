# Generated by Django 4.0.6 on 2022-11-18 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('thumbnail', models.ImageField(upload_to='column_thumbnial/%Y-%m-%d/', verbose_name='썸네일')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
            ],
            options={
                'verbose_name': '칼럼',
                'verbose_name_plural': '칼럼',
                'db_table': 'Column',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000, verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
            ],
            options={
                'verbose_name': '댓글',
                'verbose_name_plural': '댓글',
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='추천수')),
            ],
            options={
                'verbose_name': '커뮤니티',
                'verbose_name_plural': '커뮤니티',
                'db_table': 'Community',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='제목')),
                ('thumbnail', models.ImageField(upload_to='event_thumbnial/%Y-%m-%d/', verbose_name='썸네일')),
                ('content', models.TextField(verbose_name='내용')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='시작')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='종료')),
            ],
            options={
                'verbose_name': '행사',
                'verbose_name_plural': '행사',
                'db_table': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='summernote/%Y-%m-%d/')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('thumbnail', models.ImageField(upload_to='news_thumbnial/%Y-%m-%d/', verbose_name='썸네일')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='조회수')),
            ],
            options={
                'verbose_name': '뉴스',
                'verbose_name_plural': '뉴스',
                'db_table': 'News',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
            ],
            options={
                'verbose_name': '공지',
                'verbose_name_plural': '공지',
                'db_table': 'Notice',
                'ordering': ['-date'],
            },
        ),
    ]
