"""URLs configuration of the 'api' application v1."""

from rest_framework.routers import DefaultRouter

from django.urls import include, path

app_name = 'api'

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    # CategoriesDetail,
    # CategoriesList,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    get_token,
    signup,
    ReviewViewSet,
    CommentViewSet
)

v1_router = DefaultRouter()
router_v1 = DefaultRouter()

# v1_router.register(r'categories/(P<slug>[\w.@+-]+)', CategoriesViewSet, basename='categories')
v1_router.register(r'categories', CategoriesViewSet, basename='categories')
v1_router.register(r'genres', GenresViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')

router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="get_token"),
]
urlpatterns = [
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
    # path('v1/categories/', CategoriesList.as_view()),
    # path('v1/categories/<str:slug>/', CategoriesDetail.as_view()),
    path('v1/', include(v1_router.urls)),
]