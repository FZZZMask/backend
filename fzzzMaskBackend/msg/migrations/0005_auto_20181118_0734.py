# Generated by Django 2.1.3 on 2018-11-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msg', '0004_msg_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msg',
            name='pm25_value',
            field=models.IntegerField(null=True),
        ),
    ]
