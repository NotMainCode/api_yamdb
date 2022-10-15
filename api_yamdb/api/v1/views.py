"""URLs request handlers of the 'api' application."""

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.mixins import (
    CreateListDeleteViewSet,
    ModelViewSetWithoutPUT,
)
from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminRoleOrReadOnly,
    IsAdminRoleOrSuperUser,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CategoryViewSet(CreateListDeleteViewSet):
    """URL requests handler to 'Categories' resource endpoints."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminRoleOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(CreateListDeleteViewSet):
    """URL requests handler to 'Genres' resource endpoints."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminRoleOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(ModelViewSetWithoutPUT):
    """URL requests handler to 'Titles' resource endpoints."""

    queryset = (
        Title.objects.select_related("category")
        .prefetch_related("genre")
        .annotate(rating=Avg("reviews__score"))
        .order_by("name")
    )
    permission_classes = (IsAdminRoleOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in {"list", "retrieve"}:
            return TitleSerializerRead
        return TitleSerializerWrite


class ReviewViewSet(ModelViewSetWithoutPUT):
    """URL requests handler to 'Reviews' resource endpoints."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title_obj(self):
        return get_object_or_404(Title, pk=self.kwargs["title_id"])

    def get_queryset(self):
        title = self.get_title_obj()
        return title.reviews.select_related("author")

    def perform_create(self, serializer):
        title = self.get_title_obj()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSetWithoutPUT):
    """URL requests handler to 'Comments' resource endpoints."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_review_obj(self):
        return get_object_or_404(
            Review,
            id=self.kwargs["review_id"],
            title_id=self.kwargs["title_id"],
        )

    def get_queryset(self):
        review = self.get_review_obj()
        return review.comments.select_related("author")

    def perform_create(self, serializer):
        review = self.get_review_obj()
        serializer.save(author=self.request.user, review=review)


class UserViewset(ModelViewSetWithoutPUT):
    """URL requests handler to 'Users' resource endpoints."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminRoleOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        detail=False,
        url_path="me",
        methods=("get", "patch"),
        permission_classes=(IsAuthenticated,),
    )
    def users_me(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = UserSerializer(user)
        if request.method == "PATCH":
            data = request.data.copy()
            if request.user.role in {"moderator", "user"}:
                data.pop("role", None)
            serializer = UserSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            raise serializers.ValidationError(
                {
                    "detail": f"You do not have permission "
                    f"to modify user data: {instance.username}"
                }
            )
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@api_view(("POST",))
@permission_classes((AllowAny,))
def signup(request):
    """URL requests handler to the auth/signup/ endpoint."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.allow_user_receive_conf_code()
    serializer.save()
    email = serializer.validated_data["email"]
    user = get_object_or_404(User, email=email)
    conf_code = PasswordResetTokenGenerator().make_token(user)
    send_mail(
        subject="YaMDb confirmation code",
        message=f"Use this code to get an access token: {conf_code}",
        from_email=settings.FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(("POST",))
@permission_classes((AllowAny,))
def get_token(request):
    """URL requests handler to the auth/token/ endpoint."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    if not PasswordResetTokenGenerator().check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        raise serializers.ValidationError(
            {"confirmation_code": "Confirmation code is incorrect."}
        )
    access_token = AccessToken().for_user(user)
    return Response(
        {"access_token": str(access_token)}, status=status.HTTP_200_OK
    )
