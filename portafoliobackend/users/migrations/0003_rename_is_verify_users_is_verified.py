# Generated by Django 3.2.13 on 2022-06-05 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_is_verify'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='is_verify',
            new_name='is_verified',
        ),
    ]