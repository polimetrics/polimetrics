# Generated by Django 2.2 on 2019-04-25 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190425_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidatemeansentiment',
            old_name='total_favorites',
            new_name='total_engagement',
        ),
        migrations.RemoveField(
            model_name='candidatemeansentiment',
            name='total_retweets',
        ),
    ]
