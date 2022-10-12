"""URLs request handlers of the 'api' application."""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.conf_code import check_conf_code, make_conf_code
from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminRoleOrSuperUser,
    IsAdminRoleSuperUserOrReadOnly,
)
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
    CreateListDeleteViewSet,
    CreateListViewSet,
    ModelViewSetWithoutPUT,
    RetrieveUpdate,
    RetrieveUpdateDestroyViewSet,
)
from reviews.models import Categories, Genres, Review, Title
from users.models import User


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminRoleSuperUserOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminRoleSuperUserOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(ModelViewSetWithoutPUT):
    queryset = Title.objects.select_related("category").prefetch_related(
        "genre"
    )
    permission_classes = (IsAdminRoleSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializer
        return TitleSerializerAdd


class ReviewViewSet(ModelViewSetWithoutPUT):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        return title.reviews.select_related("author")

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSetWithoutPUT):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs["review_id"])
        return review.comments.select_related("author")

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs["review_id"], title=self.kwargs["title_id"]
        )
        serializer.save(author=self.request.user, review=review)


class UsersViewset(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminRoleOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)


class UsersNameViewset(RetrieveUpdateDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UsersNameSerializer
    permission_classes = (IsAdminRoleOrSuperUser,)
    lookup_field = "username"

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
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data["email"]
        if not User.objects.filter(email=email).exists():
            serializer.save(email_confirmed=True)
        make_conf_code(email)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=request.data["username"])
        if not check_conf_code(user, request.data["confirmation_code"]):
            raise serializers.ValidationError(
                {"confirmation_code": "Confirmation code is incorrect."}
            )
        access_token = RefreshToken.for_user(user).access_token
        user.email_confirmed = True
        user.save()
        return Response(
            {"access_token": str(access_token)}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
