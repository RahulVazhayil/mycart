# Generated by Django 4.1.1 on 2023-02-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_customer_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('LEE', 'LEE'), ('ALLENSOLLY', 'ALLENSOLLY'), ('APPLE', 'APPLE'), ('SAMSUNG', 'SAMSUNG'), ('REDMI', 'REDMI')], max_length=15),
        ),
    ]
