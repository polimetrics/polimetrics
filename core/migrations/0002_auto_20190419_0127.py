# Generated by Django 2.2 on 2019-04-19 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('header', models.CharField(max_length=100)),
                ('bio', models.TextField(max_length=1000)),
                ('image', models.ImageField(blank=True, upload_to='core/static/img')),
                ('fav_album', models.CharField(max_length=75)),
                ('fav_coffee', models.CharField(max_length=50)),
                ('fav_president', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='lastName',
            new_name='last_name',
        ),
    ]