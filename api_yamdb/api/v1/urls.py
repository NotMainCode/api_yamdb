from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.routers import RouterWithoutPK
from api.v1.views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    ReviewViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1_without_pk = RouterWithoutPK()
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1_without_pk.register(r'categories/(?P<slug>[\w.@+-]+)', CategoriesViewSet, basename='categories')

router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1_without_pk.register(r'genres/(?P<slug>[\w.@+-]+)', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router_v1_without_pk.urls)),
]
