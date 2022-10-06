from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.mixins import DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination

from api.v1.serializers import CategoriesSerializer, GenresSerializer, TitleSerializer
from reviews.models import Categories, Genres, Title


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
# class CategoriesList(generics.ListCreateAPIView):
#     queryset = Categories.objects.all()
#     serializer_class = CategoriesSerializer
#
#
# class CategoriesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Categories.objects.all()
#     serializer_class = CategoriesSerializer
#
#     def perform_destroy(self, instance):(self,instance):
#         instance = self.get_object()
#         return
#     # lookup_field = ['slug']


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination


