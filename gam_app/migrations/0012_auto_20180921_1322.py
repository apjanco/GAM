# Generated by Django 2.0.1 on 2018-09-21 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gam_app', '0011_auto_20180921_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagen',
            name='item',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Item'),
            preserve_default=False,
        ),
    ]