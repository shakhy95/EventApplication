# Generated by Django 2.1.1 on 2018-12-15 23:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('matchings', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 15, 23, 26, 19, 610270, tzinfo=utc)),
            preserve_default=False,
        ),
    ]