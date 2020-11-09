# Generated by Django 3.1.1 on 2020-10-08 08:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0031_videoconference'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscheckedin',
            name='check_ins_today',
            field=models.ManyToManyField(related_name='checked_in_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
