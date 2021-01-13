"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path

from rest_framework.documentation import include_docs_urls
from rest_framework import schemas

# from rest_framework_swagger.views import get_swagger_view # swagger spec.
# drf_yasg starts
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# drf_yasg ends

API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for creating and editing blog posts.'
# schema_view = get_swagger_view(title=API_TITLE)           # swagger spec.

# drf_yasg starts
schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        # terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="corto@ya.org"),
        license=openapi.License(name="BSD"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# drf_yasg ends

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/rest-auth/', include('rest_auth.urls')),

    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),

    # path('api/swagger-docs/', schema_view),               # swagger spec.

    path('api/openapi', schemas.get_schema_view(title=API_TITLE,
                                                description=API_DESCRIPTION,
                                                version="1.0.0"),
         name='openapi-schema'),

    re_path(r'^api/doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
