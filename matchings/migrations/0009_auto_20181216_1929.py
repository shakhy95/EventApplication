# Generated by Django 2.1.1 on 2018-12-16 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchings', '0008_event_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='place',
            new_name='location',
        ),
    ]
