# Generated by Django 3.2.6 on 2023-03-28 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0002_city_name'),
        ('shop', '0002_auto_20230328_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shops', to='city.city', verbose_name='Город'),
        ),
    ]
