# Generated by Django 3.2 on 2022-07-01 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_prouduct_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='catagory',
        ),
    ]
