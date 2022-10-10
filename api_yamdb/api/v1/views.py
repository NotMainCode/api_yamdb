"""URLs request handlers of the 'api' application."""

from django.shortcuts import get_object_or_404
from rest_framework import filters, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.conf_code import check_conf_code, make_conf_code
from api.v1.permissions import IsSuperuserOrAdminRole
from api.v1.serializers import (
    GetTokenSerializer,
    SignUpSerializer,
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
from users.models import User


class UsersViewset(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsSuperuserOrAdminRole,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    def perform_create(self, serializer):
        serializer.save()


class UsersNameViewset(RetrieveUpdateDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UsersNameSerializer
    permission_classes = (IsSuperuserOrAdminRole,)
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
