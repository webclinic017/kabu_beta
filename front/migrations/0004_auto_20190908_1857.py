# Generated by Django 2.2.4 on 2019-09-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20190908_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yeardata',
            name='year_profits',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='yeardata',
            name='year_sells',
            field=models.FloatField(default=0),
        ),
    ]
