import django_filters
from reviews.models import Title, Genres, Categories


# class GenresFilter(django_filters.FilterSet):
#     class Meta:
#         model = Genres
#         fields = ('slug',)
class GenresFilter(django_filters.FilterSet):
    genre = django_filters.ModelChoiceFilter(field_name='genre',
                                             to_field_name='slug',
                                             queryset=Genres.objects.all())
    category = django_filters.ModelChoiceFilter(field_name='category',
                                                to_field_name='slug',
                                                queryset=Categories.objects.all())
    # name = django_filters.ModelChoiceFilter(field_name='name',
    #                                         to_field_name='name',
    #                                         queryset=Title.objects.all())

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')




#
# class CategoriesFilter(django_filters.FilterSet):
#     category = django_filters.ModelChoiceFilter(field_name='category',
#                                                 to_field_name='slug',
#                                                 queryset=Categories.objects.all())
#
#     class Meta:
#         model = Title
#         fields = ('category',)

