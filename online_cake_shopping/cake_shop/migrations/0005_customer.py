# Generated by Django 5.0.1 on 2024-01-13 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_shop', '0004_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('phno', models.CharField(max_length=200)),
            ],
        ),
    ]