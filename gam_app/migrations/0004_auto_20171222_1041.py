# Generated by Django 2.0 on 2017-12-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gam_app', '0003_auto_20171220_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
