from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    # CategoriesDetail,
    # CategoriesList,
)

app_name = 'api'

v1_router = DefaultRouter()

# v1_router.register(r'categories/(P<slug>[\w.@+-]+)', CategoriesViewSet, basename='categories')
v1_router.register(r'categories', CategoriesViewSet, basename='categories')
v1_router.register(r'genres', GenresViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')


urlpatterns = [
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
    # path('v1/categories/', CategoriesList.as_view()),
    # path('v1/categories/<str:slug>/', CategoriesDetail.as_view()),
    path('v1/', include(v1_router.urls)),
]
