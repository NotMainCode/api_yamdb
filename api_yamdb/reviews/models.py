"""Database settings of the 'Reviews' application."""

from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    objects = models.Manager()

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    objects = models.Manager()

    def __str__(self):
        return self.name



class Title(models.Model):
    name = models.CharField(
        max_length=256
    )
    year = models.IntegerField()
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = models.Manager()



class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="ID произведения",
    )
    text = models.TextField(
        verbose_name="Текст отзыва", help_text="Напишите текст отзыва"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.PositiveIntegerField(
        verbose_name="Оценка", help_text="Оцените произведение от 1 до 10"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата отзыва", auto_now_add=True
    )

    class Meta:
        ordering = ["pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="ID отзыва",
    )
    text = models.TextField(
        verbose_name="Текст комментария", help_text="Введите текст комментария"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата комментария",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["pub_date"]
