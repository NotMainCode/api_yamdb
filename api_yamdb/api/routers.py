"""Custom routers."""

from rest_framework.routers import DefaultRouter, Route


class RouterWithoutPK(DefaultRouter):
    routes = (
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    )

