# Generated by Django 2.0.7 on 2018-07-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0007_auto_20180716_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(),
        ),
    ]