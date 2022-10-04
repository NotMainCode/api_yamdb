"""URLs configuration of the 'api' application v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from api.v1.views import (
#
# )

router_v1 = DefaultRouter()

# router_v1.register(...)
# router_v1.register(...)
# router_v1.register(...)
# router_v1.register(...)

urlpatterns = [
    path("", include(router_v1.urls)),
    # path("", include("...urls.jwt")),
]
