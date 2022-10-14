"""Custom filters."""

import django_filters
from django_filters import CharFilter, ModelChoiceFilter

from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    """'Title' resource content display filter."""

    name = CharFilter(lookup_expr="icontains")
    category = ModelChoiceFilter(
        field_name="category",
        to_field_name="slug",
        queryset=Category.objects.all(),
    )
    genre = ModelChoiceFilter(
        field_name="genre",
        to_field_name="slug",
        queryset=Genre.objects.all(),
    )
    year = CharFilter(lookup_expr="exact")

    class Meta:
        model = Title
        fields = ["name", "category", "genre", "year"]
