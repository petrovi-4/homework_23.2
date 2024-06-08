from django.db import models

from config.settings import NULLABLE
from users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Нименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', **NULLABLE,verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_modified_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    is_published = models.BooleanField(default=False, verbose_name='Опубликован')  # Добавлен признак публикации.

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('can_edit_description', 'Can edit description'),
            ('can_edit_category', 'Can edit category'),
            ('can_canceled_publication', 'Can canceled publication')
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.CharField(max_length=10, verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(verbose_name='Активная версия')

    def __str__(self):
        return f'{self.number} {self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
