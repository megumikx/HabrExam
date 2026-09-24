from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField("Название", max_length=100)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField("Название", max_length=100)
    anons = models.CharField("Название", max_length=250)
    full_text = models.TextField("Статья")
    data = models.DateTimeField("Дата публикации")

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name="Категория",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news", null=True, blank=True
    )
    image = CloudinaryField("Изображение", blank=True, null=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=[
            ('pending', 'На проверке'),
            ('approved', 'Одобрено'),
            ('rejected', 'Отклонено'),
        ],
        default='pending'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/news/{self.pk}"

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "news")

    def __str__(self):
        return f"{self.user.username} — {self.news.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ("user", "news")

    def __str__(self):
        return f"{self.user.username} — {self.news.title}: {self.value}"
