"""URLs configuration of the 'api' application v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    get_token,
    ReviewViewSet,
    signup,
    TitleViewSet,
    UserViewset,
)

router_v1 = DefaultRouter()

router_v1.register("categories", CategoryViewSet, basename="categories")

router_v1.register("genres", GenreViewSet, basename="genres")

router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)" r"/comments",
    CommentViewSet,
    basename="comments",
)

router_v1.register("users", UserViewset, basename="users")

urlpatterns = [
    path("", include(router_v1.urls)),
    path(
        "auth/",
        include(
            [
                path("signup/", signup, name="signup"),
                path("token/", get_token, name="get_token"),
            ]
        ),
    ),
]
