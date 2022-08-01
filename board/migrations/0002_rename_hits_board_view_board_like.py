# Generated by Django 4.0.6 on 2022-08-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='hits',
            new_name='view',
        ),
        migrations.AddField(
            model_name='board',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='추천수'),
        ),
    ]
