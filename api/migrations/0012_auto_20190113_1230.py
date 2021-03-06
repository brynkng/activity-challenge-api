# Generated by Django 2.1.4 on 2019-01-13 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190113_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitioninvitation',
            name='sender',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='sender_profile', to='api.Profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='competitioninvitation',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='api.Profile'),
        ),
    ]
