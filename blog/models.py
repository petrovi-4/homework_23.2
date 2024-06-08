from django.db import models
from pytils.translit import slugify

from config.settings import NULLABLE


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, max_length=100)
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(**NULLABLE, upload_to='blog_images/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
