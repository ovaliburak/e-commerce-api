# Generated by Django 3.2 on 2022-07-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20220701_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verify',
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
