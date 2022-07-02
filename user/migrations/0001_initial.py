# Generated by Django 3.2 on 2022-06-30 20:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(db_index=True, max_length=100)),
                ('last_name', models.CharField(db_index=True, max_length=100)),
            
            ],
            options={
                'abstract': False,
            },
        ),
    ]