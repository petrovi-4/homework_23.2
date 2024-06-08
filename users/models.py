import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    token = models.CharField(max_length=50, unique=True, **NULLABLE)  # Добавил токен в моедль пользователя.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
