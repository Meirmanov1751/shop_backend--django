# Generated by Django 3.2.6 on 2023-03-30 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseAboutApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Отзыв')),
                ('status', models.IntegerField(choices=[(0, 'В обработке'), (1, 'В пути'), (2, 'Завершено')], default=0, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')),
            ],
            options={
                'verbose_name': 'Отзыв о приложении',
                'verbose_name_plural': 'Отзывы о приложении',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('flutter', 'Flutter'), ('ios', 'ios'), ('android', 'android')], max_length=150, unique=True)),
                ('version', models.CharField(max_length=120)),
                ('hard', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Версия приложения',
                'verbose_name_plural': 'Версия приложения',
            },
        ),
    ]
