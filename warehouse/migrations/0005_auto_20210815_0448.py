# Generated by Django 3.0.8 on 2021-08-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20210814_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
