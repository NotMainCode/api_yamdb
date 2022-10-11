"""Serializers of the 'api' application."""

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from users.models import User


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
            and User.objects.get(email=value).is_active
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
            and User.objects.get(username=value).is_active
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
