"""URLs configuration of the 'api' application v1."""

from django.urls import include, path

from api.routers import RouterWithoutPKandPUT
from api.v1.views import (
    get_token,
    signup,
    UsersMeViewset,
    UsersNameViewset,
    UsersViewset,
)

router_users_v1 = RouterWithoutPKandPUT()

router_users_v1.register(r"users", UsersViewset, basename="users")
router_users_v1.register(r"users/me", UsersMeViewset, basename="users_me")
router_users_v1.register(
    r"users/(?P<username>[\w.@+-]+)",
    UsersNameViewset,
    basename="users_name",
)

urlpatterns = [
    path("", include(router_users_v1.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="get_token"),
]
