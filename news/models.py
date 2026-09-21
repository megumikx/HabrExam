from django.db import models
from cloudinary.models import CloudinaryField

class News(models.Model):
    CATEGORY_CHOICES = [
    ('backend', 'Бэкенд'),
    ('frontend', 'Фронтенд'),
    ('ai', 'Искусственный интеллект'),
    ('cyber_security', 'Кибербезопасность'),
    ('cyber_sport', 'Киберспорт'),
    ('game_development', 'Разработка игр'),
    ('other', 'Разное'),
]

    title = models.CharField('Название', max_length=100)
    anons = models.CharField('Название', max_length=250)
    full_text = models.TextField('Статья')
    data = models.DateTimeField('Дата публикации')
    category = models.CharField('Категория', max_length=35, choices=CATEGORY_CHOICES)
    image = CloudinaryField('Изображение', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.pk}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'