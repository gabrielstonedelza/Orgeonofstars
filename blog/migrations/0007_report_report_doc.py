# Generated by Django 3.0.6 on 2020-07-31 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200731_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_doc',
            field=models.FileField(blank=True, upload_to='report_documents'),
        ),
    ]
