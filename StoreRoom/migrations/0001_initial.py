# Generated by Django 3.2.8 on 2021-10-21 06:06

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50, unique=True, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('details', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Product Details')),
                ('keywords', models.TextField(blank=True, null=True, verbose_name='Keywords')),
                ('label', models.CharField(choices=[('Sale', 'Sale'), ('New', 'New'), ('Promotion', 'Promotion'), ('Make4Me Special', 'Make4Me Special')], max_length=20, verbose_name='Label')),
                ('inStock', models.PositiveIntegerField(verbose_name='In Stock')),
                ('isAvailable', models.BooleanField(default=True)),
                ('highPrice', models.FloatField(verbose_name='High Price')),
                ('discountedPrice', models.FloatField(blank=True, verbose_name='Selling Price')),
                ('tax', models.PositiveSmallIntegerField(default=0, verbose_name='Tax')),
                ('shippingCharge', models.FloatField(default=0, verbose_name='Shipping Charge')),
                ('productImage', models.ImageField(upload_to='Images/ProductImages/')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('soldCount', models.PositiveIntegerField(default=0, verbose_name='Sold Count')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Category.category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sliderImage', models.ImageField(help_text='Size: 900 X 1920', upload_to='Images/SliderImages/', verbose_name='Slider Image')),
                ('punchLine_1', models.CharField(max_length=100, verbose_name='PunchLine 1')),
                ('punchLine_2', models.CharField(blank=True, max_length=100, verbose_name='PunchLine 2')),
                ('pickUpLine', models.CharField(blank=True, max_length=100, verbose_name='Pick Up Line')),
                ('startingAt', models.CharField(blank=True, max_length=100, verbose_name='Starting From')),
                ('url', models.URLField(null=True, verbose_name='URL')),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewAndRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100, verbose_name='Subject')),
                ('review', models.TextField(blank=True, max_length=500, verbose_name='Review')),
                ('rating', models.FloatField(verbose_name='Rating Star')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP Address Of User')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modifiedAt', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreRoom.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review And Rating',
                'verbose_name_plural': 'Reviews And Ratings',
            },
        ),
        migrations.CreateModel(
            name='ProductVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variationCategory', models.CharField(choices=[('Color', 'Color'), ('Size', 'Size')], max_length=50, verbose_name='Type Of Variation')),
                ('isActive', models.BooleanField(default=True, verbose_name='Is Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('variationValue', models.CharField(max_length=100, verbose_name='Enter Size Or Color')),
                ('productImage', models.ImageField(blank=True, upload_to='Images/ProductImages/')),
                ('highPrice', models.FloatField(verbose_name='High Price')),
                ('discountedPrice', models.FloatField(blank=True, verbose_name='Selling Price')),
                ('keywords', models.TextField(blank=True, null=True, verbose_name='Keywords')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreRoom.product')),
            ],
            options={
                'verbose_name': 'Product Variant',
                'verbose_name_plural': 'Product Variants',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productImage', models.ImageField(max_length=255, upload_to='Images/ProductImages/', verbose_name='Product Image')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='StoreRoom.product')),
            ],
            options={
                'verbose_name': 'Product Image Gallery',
                'verbose_name_plural': 'Product Image Gallery',
            },
        ),
        migrations.CreateModel(
            name='ProductCustomization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customizationImage', models.ImageField(upload_to='Images/CustomizationImages/', verbose_name='Customization Image')),
                ('cutomizationNotes', models.TextField(blank=True, max_length=300, verbose_name='Cutomization Notes')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='StoreRoom.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]