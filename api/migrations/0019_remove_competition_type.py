# Generated by Django 2.1.4 on 2019-02-03 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20190202_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='type',
        ),
    ]