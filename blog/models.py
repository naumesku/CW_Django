from django.db import models
from config_my import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    img = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    data_create = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовкано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
