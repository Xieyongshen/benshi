# Generated by Django 2.0.7 on 2018-07-18 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0010_service_servicedetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followTagName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calc.Tag'),
        ),
    ]
