# Generated by Django 2.0.2 on 2018-03-05 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20180305_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='event',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]