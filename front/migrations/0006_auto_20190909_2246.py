# Generated by Django 2.2.4 on 2019-09-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_dailydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailydata',
            name='buy_signal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='day_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='fiveday_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='sale_signal',
            field=models.IntegerField(default=0),
        ),
    ]
