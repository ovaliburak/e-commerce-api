# Generated by Django 3.2 on 2022-07-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_rename_prouduct_discount_product_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_inventory',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ProductInventory',
        ),
    ]
