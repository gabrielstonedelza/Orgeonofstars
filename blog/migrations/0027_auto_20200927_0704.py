# Generated by Django 3.1.1 on 2020-09-27 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_auto_20200927_0703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userscheckedin',
            old_name='date_posted',
            new_name='date_checked_in',
        ),
    ]
