# Generated by Django 3.2.23 on 2023-11-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify', '0009_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='shipping_cost',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
