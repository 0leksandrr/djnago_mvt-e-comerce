# Generated by Django 5.1.4 on 2024-12-24 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_alter_category_options_alter_category_cat_image_and_more'),
        ('store', '0012_alter_product_product_name_alter_product_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товари'},
        ),
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'Галерея товарів'},
        ),
        migrations.AlterModelOptions(
            name='reviewrating',
            options={'verbose_name': 'Відгук та оцінка', 'verbose_name_plural': 'Відгуки та оцінки'},
        ),
        migrations.AlterModelOptions(
            name='variation',
            options={'verbose_name': 'Варіацію', 'verbose_name_plural': 'Варіації'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Доступний'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата змін'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, upload_to='photos/products', verbose_name='Фото товару'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Назва товару'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='ip',
            field=models.CharField(blank=True, max_length=20, verbose_name='IP адреса'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='review',
            field=models.TextField(blank=True, max_length=500, verbose_name='Відгук'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата оновлення'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='created_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата створення'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'колір'), ('size', 'розмір')], max_length=100, verbose_name='Категорія варіації'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=100, verbose_name='Значення варіації'),
        ),
    ]
