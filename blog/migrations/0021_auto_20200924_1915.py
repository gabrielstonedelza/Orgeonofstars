# Generated by Django 3.1.1 on 2020-09-24 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20200924_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifyme',
            old_name='follower_sender',
            new_name='sender',
        ),
        migrations.DeleteModel(
            name='LoginCode',
        ),
    ]