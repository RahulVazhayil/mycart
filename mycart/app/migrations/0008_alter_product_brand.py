# Generated by Django 4.1.1 on 2023-02-19 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_product_brand_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('LEE', 'LEE'), ('ALLENSOLLY', 'ALLENSOLLY'), ('APPLE', 'APPLE'), ('SAMSUNG', 'SAMSUNG'), ('REDMI', 'REDMI'), ('ASUS', 'ASUS'), ('DELL', 'DELL'), ('ACER', 'ACER'), ('ONEPLUS', 'ONEPLUS'), ('LG', 'LG'), ('LENOVO', 'LENOVO'), ('NOKIA', 'NOKIA'), ('MOTOROLA', 'MOTOROLA'), ('REALME', 'REALME'), ('WOODLAND', 'WOODLAND'), ('W', 'W'), ('JOCKEY', 'JOCKEY'), ('WILDCRAFT', 'WILDCRAFT'), ('HP', 'HP')], max_length=15),
        ),
    ]
