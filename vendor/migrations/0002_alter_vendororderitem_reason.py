# Generated by Django 4.2 on 2024-05-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendororderitem',
            name='reason',
            field=models.IntegerField(blank=True, choices=[(0, 'Out of Stock'), (1, 'Price Difference'), (2, 'other')], null=True),
        ),
    ]