# Generated by Django 4.0.6 on 2022-11-10 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_exp_user_level_user_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='level',
            new_name='lv',
        ),
    ]