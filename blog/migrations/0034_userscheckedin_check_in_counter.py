# Generated by Django 3.1.1 on 2020-10-08 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_remove_userscheckedin_check_ins_today'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscheckedin',
            name='check_in_counter',
            field=models.IntegerField(default=0),
        ),
    ]
