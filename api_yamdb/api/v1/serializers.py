"""Serializers of the 'api' application."""

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Genres, Title
from rest_framework import serializers

from users.models import User
from reviews.models import Review, Comment


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


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f"Another user is already using mail: {value}."
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f"User named '{value}' already exists."
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f"The user named '{value}' does not exist."
            )
        return value

    def validate_confirmation_code(self, value):
        if len(value) < 32:
            raise serializers.ValidationError(
                "Ensure that confirmation code contain 32 characters."
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, attrs):
        pass

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, attrs):
        pass

    class Meta:
        model = Comment
        fields = '__all__'
