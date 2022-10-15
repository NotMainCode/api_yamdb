"""Serializers of the 'api' application."""

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def unacceptable_username(username):
    return username.lower() == settings.UNACCEPTABLE_USERNAME


def email_exists(email):
    return User.objects.filter(email=email).exists()


def username_exists(username):
    return User.objects.filter(username=username).exists()


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
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if request.method != "POST":
            return data
        if Review.objects.filter(
            title=title_id, author=request.user
        ).exists():
            raise ValidationError(
                """You can only leave one review for this creation."""
            )
        else:
            return data


    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]


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
        if unacceptable_username(value):
            raise serializers.ValidationError("The name 'me' is not allowed.")
        return value


class SignUpSerializer(serializers.Serializer):
    """Serializer for requests to auth/signup/ endpoint."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)

    def allow_user_receive_conf_code(self):
        email = self.validated_data["email"]
        username = self.validated_data["username"]
        if email_exists(email) and username_exists(username):
            return
        if username_exists(username):
            raise serializers.ValidationError(
                f"User named '{username}' already exists."
            )
        if email_exists(email):
            raise serializers.ValidationError(
                f"Another user is already using mail: {email}."
            )
        if unacceptable_username(username):
            raise serializers.ValidationError("The name 'me' is not allowed.")


class GetTokenSerializer(serializers.Serializer):
    """Serializer for requests to auth/token/ endpoint."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    def validate_username(self, value):
        if not username_exists(value):
            raise NotFound(detail=f"The user named '{value}' does not exist.")
        return value

    def validate_confirmation_code(self, value):
        if len(value) != 24:
            raise serializers.ValidationError(
                "Ensure that confirmation code contain 24 characters."
            )
        return value
