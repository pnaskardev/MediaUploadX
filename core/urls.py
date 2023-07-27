"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(title="MediaCMS API", default_version='v1', contact=openapi.Contact(
        url="https://mediacms.io"), x_logo={"url": "../../static/images/logo_dark.svg"}),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    re_path(r"^", include("users.urls")),
    re_path(r"^", include("files.urls")),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^api-auth/", include("rest_framework.urls")),
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('docs/api/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
