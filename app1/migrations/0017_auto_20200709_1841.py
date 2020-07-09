# Generated by Django 3.0.3 on 2020-07-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_auto_20200709_1827'),
    ]

    operations = [
        migrations.DeleteModel(
            name='complaint',
        ),
        migrations.AddField(
            model_name='pothole',
            name='origin',
            field=models.CharField(blank='True', default='', max_length=32),
        ),
        migrations.AddField(
            model_name='pothole',
            name='pothole_image',
            field=models.ImageField(blank='True', upload_to='pothole_pictures'),
        ),
    ]
