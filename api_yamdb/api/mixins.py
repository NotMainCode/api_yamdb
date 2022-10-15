"""Custom viewsets."""

from rest_framework import mixins, viewsets


class CreateListDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset allows methods: GET(queryset), POST, DELETE."""

    pass


class ModelViewSetWithoutPUT(viewsets.ModelViewSet):
    """The viewset allows all methods except PUT."""

    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    pass
