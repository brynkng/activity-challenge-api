# Generated by Django 2.1.4 on 2019-01-24 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20190124_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitionscore',
            name='user',
        ),
        migrations.AddField(
            model_name='competitionscore',
            name='profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Profile'),
            preserve_default=False,
        ),
    ]
