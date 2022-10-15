"""Admin site settings of the 'Reviews' application."""

from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Table settings for categories on the admin site."""

    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("name",)


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """Table settings for genres on the admin site."""

    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Table settings for creations on the admin site."""

    list_display = (
        "pk",
        "name",
        "year",
        "category",
        "description",
    )
    list_editable = ("category",)
    search_fields = ("name", "year")
    list_filter = ("category",)
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Table settings for creations reviews on the admin site."""

    list_display = (
        "pk",
        "title_id",
        "score",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("title_id",)
    list_filter = ("author", "score")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Table settings for comments on reviews on the admin site."""

    list_display = (
        "pk",
        "review_id",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("review_id",)
    list_filter = ("author",)
