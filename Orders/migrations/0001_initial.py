# Generated by Django 3.2.8 on 2021-10-21 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('StoreRoom', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNumber', models.CharField(max_length=20, verbose_name='Order Number')),
                ('paymentMethod', models.CharField(blank=True, max_length=150, verbose_name='Payment Method')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('address_line_1', models.CharField(max_length=100, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=100, verbose_name='Address Line 2')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('state', models.CharField(max_length=50, verbose_name='State')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('pincode', models.CharField(max_length=10, verbose_name='Pincode')),
                ('order_note', models.TextField(blank=True, max_length=250, verbose_name='Order Note')),
                ('orderTotal', models.FloatField(verbose_name='Order Total')),
                ('tax', models.FloatField(verbose_name='Tax')),
                ('orderStatus', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10, verbose_name='Order Status')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP Address')),
                ('isOrdered', models.BooleanField(default=False, verbose_name='Is Ordered')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentId', models.CharField(max_length=150, verbose_name='Payment ID')),
                ('paymentMethod', models.CharField(choices=[('PayPal', 'PayPal'), ('Paytm', 'Paytm'), ('RazorPay', 'RazorPay')], max_length=150, verbose_name='Payment Method')),
                ('amountPaid', models.FloatField(verbose_name='Amount Paid')),
                ('paymentStatus', models.CharField(max_length=150, verbose_name='Payment Status')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('productPrice', models.FloatField(verbose_name='Product Price')),
                ('ordered', models.BooleanField(default=False, verbose_name='Ordered')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Orders.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreRoom.product')),
                ('productVariant', models.ManyToManyField(blank=True, to='StoreRoom.ProductVariants', verbose_name='Product Variant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ordered Product',
                'verbose_name_plural': 'Ordered Products',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
