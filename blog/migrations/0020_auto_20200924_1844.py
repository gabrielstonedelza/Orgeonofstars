# Generated by Django 3.1.1 on 2020-09-24 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_post_image_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifyme',
            old_name='sender',
            new_name='follower_sender',
        ),
    ]
