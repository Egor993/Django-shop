# Generated by Django 3.1.2 on 2020-10-01 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='directors',
            new_name='author',
        ),
    ]
