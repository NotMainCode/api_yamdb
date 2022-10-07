"""URLs configuration of the 'api' application v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.routers import RouterWithoutPK
from api.v1.views import (
    get_token,
    signup,
    UsersMeViewset,
    UsersNameViewset,
    UsersViewset,
)

router_v1 = DefaultRouter()
router_v1_without_pk = RouterWithoutPK()

router_v1.register(r"users", UsersViewset, basename="users")
router_v1_without_pk.register(r"users/me", UsersMeViewset, basename="users_me")
router_v1_without_pk.register(
    r"users/(?P<username>[\w.@+-]+)",
    UsersNameViewset,
    basename="users_name",
)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include(router_v1_without_pk.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="get_token"),
]
