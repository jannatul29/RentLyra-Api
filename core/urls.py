"""
URL configuration for rentlyra_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.response import Response
from rest_framework.views import APIView


class APIVersionDocumentationView(APIView):
    """
    API version documentation for RentLyra.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response({
            "v1": request.build_absolute_uri("/v1/"),
            "schema": request.build_absolute_uri("/api/schema/"),
            "swagger": request.build_absolute_uri("/swagger/"),
            "redoc": request.build_absolute_uri("/redoc/"),
        })


urlpatterns = [
    path("", APIVersionDocumentationView.as_view(), name="api-version"),
    path("admin/", admin.site.urls),
    path("v1/", include("users.urls")),
    path("accounts/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
