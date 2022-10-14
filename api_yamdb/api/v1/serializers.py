"""Serializers of the 'api' application."""

import datetime as dt

from django.conf import settings
from django.db.models import Avg
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
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for requests 'GET' to endpoints of Titles resource."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, ob):
        return ob.reviews.all().aggregate(Avg("score"))["score__avg"]

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

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError("Please enter a valid date")
        return value


class TitleSerializerAdd(serializers.ModelSerializer):
    """Serializer for requests (excl 'GET') to 'Titles' resource endpoints."""

    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        many=False,
        required=True,
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

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError("Please enter a valid date")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Reviews' resource."""

    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        title = get_object_or_404(
            Title, pk=self.context["view"].kwargs["title_id"]
        )
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    """You can only leave one review for this creation."""
                )
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for requests to endpoints of 'Comments' resource."""

    review = serializers.SlugRelatedField(slug_field="text", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"


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
            return True
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
        return True


class GetTokenSerializer(serializers.Serializer):
    """Serializer for requests to auth/token/ endpoint."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    def validate_username(self, value):
        if not username_exists(value):
            raise NotFound(detail=f"The user named '{value}' does not exist.")
        return value

    def validate_confirmation_code(self, value):
        if len(value) < 24:
            raise serializers.ValidationError(
                "Ensure that confirmation code contain 24 characters."
            )
        return value
