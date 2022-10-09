"""URLs request handlers of the 'api' application."""
import django_filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.conf_code import check_conf_code, make_conf_code
from api.v1.filters import GenresFilter
from api.v1.permissions import IsAuthorOrReadOnly, IsRoleAdmin, ReadOnlyOrAdmin, IsAdminOrReadOnly
from api.v1.serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TitleSerializerAdd,
    UsersMeGetSerializer,
    UsersMePatchSerializer,
    UsersNameSerializer,
    UsersSerializer,
)
from api.viewsets import (
    CreateListViewSet,
    RetrieveUpdate,
    RetrieveUpdateDestroyViewSet,
)
from reviews.models import Categories, Genres, Review, Title
from users.models import User


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = "slug"
    permission_classes = (ReadOnlyOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    search_fields = ("slug",)
    permission_classes = (ReadOnlyOrAdmin,)
    filter_backends = (filters.SearchFilter,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filter_backends = (DjangoFilterBackend,)
    filter_class = GenresFilter

    # filterset_fields = ("genre",)


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSerializerAdd



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewset(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    def perform_create(self, serializer):
        if serializer.validated_data.get("role") == "admin":
            serializer.save(is_staff=True, is_active=False)
            return Response(status=status.HTTP_201_CREATED)
        serializer.save(is_active=False)


class UsersNameViewset(RetrieveUpdateDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UsersNameSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "username"

    def perform_update(self, serializer):
        if serializer.validated_data.get("role") == "admin":
            serializer.save(is_staff=True)
            return
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        if instance.is_superuser:
            raise serializers.ValidationError(
                {
                    "detail": f"You do not have permission "
                    f"to modify user data: {instance.username}"
                }
            )
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class UsersMeViewset(RetrieveUpdate):
    serializer_class = UsersMeGetSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UsersMePatchSerializer
        return UsersMeGetSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        make_conf_code(request.data["email"])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=request.data["username"])
        if not check_conf_code(user, request.data["confirmation_code"]):
            raise serializers.ValidationError(
                {"confirmation_code": "Confirmation code is incorrect."}
            )
        access_token = RefreshToken.for_user(user).access_token
        return Response(
            {"access_token": str(access_token)}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
