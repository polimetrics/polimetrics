# Generated by Django 2.2 on 2019-04-23 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', 'csv'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'ordering': ['last_name']},
        ),
    ]
