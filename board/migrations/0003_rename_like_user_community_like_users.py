# Generated by Django 4.0.6 on 2022-08-19 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_community_like_user_alter_community_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='like_user',
            new_name='like_users',
        ),
    ]
