from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Genres, Title


class CategoriesSerializer(serializers.ModelSerializer):
    # slug = serializers.SlugRelatedField(
    #     queryset=Categories.objects.all(),
    #     slug_field='slug',
    #     # read_only=True
    # )


    class Meta:
        # fields = '__all__'
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  # 'rating',
                  'description',
                  'genre',
                  'category')
        model = Title
