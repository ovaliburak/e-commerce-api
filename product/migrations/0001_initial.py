# Generated by Django 3.2 on 2022-07-01 16:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('discount_percent', models.FloatField()),
                ('discount_quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True)),
                ('active', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('price', models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=6)),
                ('is_listable', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='product.category')),
                ('product_inventory', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='product.productinventory')),
                ('prouduct_discount', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='product.productdiscount')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]
