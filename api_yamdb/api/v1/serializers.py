"""Serializers of the 'api' application."""

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def unacceptable_username(username):
    if username.lower() == settings.UNACCEPTABLE_USERNAME:
        raise serializers.ValidationError(
            f"The name {settings.UNACCEPTABLE_USERNAME} is not allowed."
        )


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Categories' resource."""

    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Genres' resource."""

    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializerRead(serializers.ModelSerializer):
    """Serializer for requests 'GET' to endpoints of Titles resource."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleSerializerWrite(serializers.ModelSerializer):
    """Serializer for requests (excl 'GET') to 'Titles' resource endpoints."""

    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), many=False
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Reviews' resource."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        if request.method != "POST":
            return data
        if Review.objects.filter(
            title_id=title_id, author=request.user
        ).exists():
            raise ValidationError(
                """You can only leave one review for this creation."""
            )
        else:
            return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Comments' resource."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class UserSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Users' resource."""

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, value):
        unacceptable_username(value)
        return value


class SignUpSerializer(serializers.Serializer):
    """Serializer for requests to auth/signup/ endpoint."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        unacceptable_username(value)
        return value


class GetTokenSerializer(serializers.Serializer):
    """Serializer for requests to auth/token/ endpoint."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=24)

    def validate_username(self, value):
        unacceptable_username(value)
        return value
