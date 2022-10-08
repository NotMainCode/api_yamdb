"""Database settings of the 'Reviews' application."""

from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Категория",
        help_text="Укажите категорию"
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="URL категории",
        help_text="Укажите URL категории"
    )

    objects = models.Manager()

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Жанр",
        help_text="Укажите жанр"
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="URL жанра",
        help_text="Укажите URL жанра"
    )

    objects = models.Manager()

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        help_text="Укажите название"
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        help_text="Укажите год выпуска"
    )

    # rating = models.ForeignKey(
    #     'Review',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="reviews",
    # )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Укажите описание (необязательно к заполнению)"
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name="Жанр",
        help_text="Выберите жанр",
        related_name='title'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        verbose_name="Категория",
        help_text="Выберите категорию",
        related_name='title'
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
