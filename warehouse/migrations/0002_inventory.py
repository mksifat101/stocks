# Generated by Django 3.0.8 on 2021-08-14 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('weight', models.IntegerField()),
                ('count', models.BigIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.Item')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.Warehouse')),
            ],
        ),
    ]
