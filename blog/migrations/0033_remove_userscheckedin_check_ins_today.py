# Generated by Django 3.1.1 on 2020-10-08 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_userscheckedin_check_ins_today'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userscheckedin',
            name='check_ins_today',
        ),
    ]