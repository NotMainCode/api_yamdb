from django.db import models


class Categories(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    # objects = models.Manager()

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
    # rating = Рейтинг на основе отзывов, если отзывов нет — `None`
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(Genres)
    # genre = models.ForeignKey(
    #     Genres,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = models.Manager()
