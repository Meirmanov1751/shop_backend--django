# Generated by Django 3.2.6 on 2023-03-29 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_shopworktime_options'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopOrder',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='ShopOrderItem',
            new_name='OrderItem',
        ),
    ]
