# Generated by Django 3.2.8 on 2021-10-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='imageForCustomization',
            field=models.ImageField(null=True, upload_to='Images/CustomizationImages/', verbose_name='Image For Customization'),
        ),
    ]
