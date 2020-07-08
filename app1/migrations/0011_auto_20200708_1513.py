# Generated by Django 3.0.3 on 2020-07-08 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20200708_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='uploaded_timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='pothole',
            name='completed_timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='pothole',
            name='ongoin_timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='pothole',
            name='uploaded_timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='twitter_data',
            name='tweet_id',
            field=models.CharField(blank='True', default='', max_length=256),
        ),
    ]
