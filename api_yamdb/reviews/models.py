"""Database settings of the 'Reviews' application."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User


class Category(models.Model):
    """'Category' resource table settings."""

    name = models.CharField(
        max_length=256,
        verbose_name="Category",
        help_text="Enter a category",
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Category URL",
        help_text="Enter the category URL",
    )

    class Meta:
        ordering = ("name", "slug")
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """'Genre' resource table settings."""

    name = models.CharField(
        max_length=256,
        verbose_name="Genre",
        help_text="Enter the genre",
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Genre URL",
        help_text="Enter the genre URL",
    )

    class Meta:
        ordering = ("name", "slug")
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name


class Title(models.Model):
    """'Title' resource table settings."""

    name = models.CharField(
        max_length=256,
        verbose_name="Title",
        help_text="Enter the title",
        db_index=True,
    )
    year = models.PositiveIntegerField(
        verbose_name="Release year",
        help_text="Enter the release year",
        validators=(validate_year,),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description",
        help_text="Enter a description (not necessary)",
    )
    genre = models.ManyToManyField(
        Genre, verbose_name="Genres", help_text="Select a genre"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Category",
        help_text="Select a category",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "title"
        verbose_name_plural = "titles"

    def __str__(self):
        return self.name


class Review(models.Model):
    """'Review' resource table settings."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Title ID",
    )
    text = models.TextField(
        verbose_name="Review text", help_text="Write the review"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Review author",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Rating",
        help_text="Rate the creation from 1 to 10",
        validators=[
            MinValueValidator(1, "Enter a rating from 1 to 10"),
            MaxValueValidator(10, "Enter a rating from 1 to 10"),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="Review date", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            ),
        ]
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        return self.text[: settings.NUM_CHAR]


class Comment(models.Model):
    """'Comment' resource table settings."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Review ID",
    )
    text = models.TextField(
        verbose_name="Comment text", help_text="Enter the comment text"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Comment author",
    )
    pub_date = models.DateTimeField(
        verbose_name="Comment date", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return self.text[: settings.NUM_CHAR]
