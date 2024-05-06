# Generated by Django 4.2 on 2024-05-06 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_order_user_profile'),
        ('vendor', '0002_alter_vendororderitem_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.IntegerField(choices=[(0, 'Pending'), (1, 'Yes'), (2, 'No')], default=0)),
                ('fulfilment', models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Self'), (2, 'Zit Ship')], default=2)),
                ('status', models.IntegerField(choices=[(0, 'Preparing to ship'), (1, 'Shipped'), (2, 'Delivered'), (3, 'Delivery Failed'), (4, 'Canceled')], default=0)),
                ('reason', models.IntegerField(blank=True, choices=[(0, 'Out of Stock'), (1, 'Price Difference'), (2, 'other')], null=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_order_number_item', to='checkout.orderlineitem')),
            ],
        ),
        migrations.DeleteModel(
            name='VendorOrderItem',
        ),
    ]
