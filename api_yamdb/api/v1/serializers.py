from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Genres, Title, Review

import datetime as dt


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = '__all__'
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        return data


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
        required=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        many=False,
        required=True
    )

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  # 'rating',
                  'description',
                  'genre',
                  'category')
        model = Title

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Укажите корректную дату'
            )
        return value




