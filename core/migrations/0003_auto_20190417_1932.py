# Generated by Django 2.2 on 2019-04-17 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190417_1741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='last_name',
        ),
    ]