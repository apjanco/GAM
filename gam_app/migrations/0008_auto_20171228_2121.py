# Generated by Django 2.0 on 2017-12-28 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gam_app', '0007_auto_20171227_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='no_victims',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='page_count',
            field=models.IntegerField(),
        ),
    ]