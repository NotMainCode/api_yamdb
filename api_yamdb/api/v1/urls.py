"""URLs configuration of the 'api' application v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.routers import RouterWithoutPKandPUT
from api.v1.views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    get_token,
    ReviewViewSet,
    signup,
    TitleViewSet,
    UsersMeViewset,
    UsersNameViewset,
    UsersViewset,
)

app_name = "api"

router_v1 = DefaultRouter()
router_users_v1 = RouterWithoutPKandPUT()

router_users_v1.register(r"users", UsersViewset, basename="users")
router_users_v1.register(r"users/me", UsersMeViewset, basename="users_me")
router_users_v1.register(
    r"users/(?P<username>[\w.@+-]+)",
    UsersNameViewset,
    basename="users_name",
)
router_v1.register(r"categories", CategoriesViewSet, basename="categories")
router_v1.register(r"genres", GenresViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)" r"/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include(router_users_v1.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="get_token"),
]
