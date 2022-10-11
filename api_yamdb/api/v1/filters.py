"""Custom filters."""

import django_filters

from reviews.models import Title, Genres, Categories


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.ModelChoiceFilter(
        field_name='genre',
        to_field_name='slug',
        queryset=Genres.objects.all()
    )
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        to_field_name='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'genre',
            'category',
            'year'
        )
