"""Serializers of the 'api' application."""

import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories


class CategoriesSerializerAdd(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class TitleSerializerAdd(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genres.objects.all(),
        many=True,
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Categories.objects.all(),
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
            raise serializers.ValidationError("Укажите корректную дату")
        return value


class UsersSerializer(serializers.ModelSerializer):
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
        if value.lower() == "me":
            raise serializers.ValidationError("The name 'me' is not allowed.")
        return value


class UsersNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("username", "email")
        model = User


class UsersMeGetSerializer(serializers.ModelSerializer):
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


class UsersMePatchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("username", "email", "role")
        model = User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)

    def validate_email(self, value):
        if (
            User.objects.filter(email=value).exists()
            and User.objects.get(email=value).email_confirmed
        ):
            raise serializers.ValidationError(
                f"Another user is already using mail: {value}."
            )
        return value

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("The name 'me' is not allowed.")
        if (
            User.objects.filter(username=value).exists()
            and User.objects.get(username=value).email_confirmed
        ):
            raise serializers.ValidationError(
                f"User named '{value}' already exists."
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise NotFound(detail=f"The user named '{value}' does not exist.")
        return value

    def validate_confirmation_code(self, value):
        if len(value) < 32:
            raise serializers.ValidationError(
                "Ensure that confirmation code contain 32 characters."
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    """Вы можете оставить только
                                        один отзыв к этому произведению"""
                )
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(
        many=True,
    )
    category = CategoriesSerializer()
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
            raise serializers.ValidationError("Укажите корректную дату")
        return value
