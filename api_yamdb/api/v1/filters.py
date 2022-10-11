"""Custom filters."""

import django_filters
from django_filters import CharFilter, ModelChoiceFilter

from reviews.models import Categories, Genres, Title


class TitleFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr="icontains")
    category = ModelChoiceFilter(
        field_name="category",
        to_field_name="slug",
        queryset=Categories.objects.all(),
    )
    genre = ModelChoiceFilter(
        field_name="genre",
        to_field_name="slug",
        queryset=Genres.objects.all(),
    )
    year = CharFilter()

    class Meta:
        model = Title
        fields = ["name", "category", "genre", "year"]
