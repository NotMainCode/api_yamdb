"""URLs configuration of the 'api' application v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    get_token,
    signup,
)

router_v1 = DefaultRouter()

# router_v1.register(...)
# router_v1.register(...)
# router_v1.register(...)
# router_v1.register(...)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="get_token"),
]
