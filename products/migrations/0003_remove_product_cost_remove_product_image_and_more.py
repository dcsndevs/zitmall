# Generated by Django 4.2 on 2024-05-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_status_alter_product_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.AddField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, help_text='This is the first imagethat site users would see', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='image_1_alt',
            field=models.CharField(blank=True, help_text='Default Image alt text', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_2_alt',
            field=models.CharField(blank=True, help_text='Image-2 alt text', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_3_alt',
            field=models.CharField(blank=True, help_text='Image-3 alt text', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_url_alt',
            field=models.CharField(blank=True, help_text='Image url alt text', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='shipping',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Shipping fee for this product', max_digits=10),
        ),
    ]
