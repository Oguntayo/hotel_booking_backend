"""
URL configuration for hotelperhour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]



from django.urls import path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    html_content = """
    <html>
        <head>
            <title>Welcome | hotelperhour project.</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
                h1 { color: #2c3e50; }
                p { font-size: 18px; }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>Welcome to HPH API</h1>
            <p>Explore my API with swagger ui <a href='/swagger/'>here</a> 🚀</p>
        </body>
    </html>
    """
    return HttpResponse(html_content)


schema_view = get_schema_view(
    openapi.Info(
        title="Hotel Per Hour API",
        default_version='v1',
        description="Booking API docs",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Add Bearer authentication to Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "Enter 'Bearer <your_token>' to authenticate",
        }
    },
    'USE_SESSION_AUTH': False,  # Disables Django session authentication
}


urlpatterns = [
    path('', home, name="home"),
    
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    # Swagger Endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)