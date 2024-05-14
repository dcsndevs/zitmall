# Generated by Django 4.2 on 2024-05-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_orderlineitem_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='shipping',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True),
        ),
    ]
