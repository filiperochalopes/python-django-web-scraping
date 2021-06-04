"""app URL Configuration

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
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.schemas import get_schema_view

from app.core.views import UserViewSet, GroupViewSet, scraping_dentalspeed_selenium, scraping_dentalspeed_scrapy,  scraping_dentalspeed_rpa, scraping_dentalcremer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    re_path(r'api/v1/scraping/dentalspeed/(?P<query>[-\w]+)/selenium', scraping_dentalspeed_selenium),
    re_path(r'api/v1/scraping/dentalspeed/(?P<query>[-\w]+)/scrapy', scraping_dentalspeed_scrapy),
    re_path(r'api/v1/scraping/dentalspeed/(?P<query>[-\w]+)/rpa', scraping_dentalspeed_rpa),
    re_path(r'api/v1/scraping/dentalcremer/(?P<query>[-\w]+)', scraping_dentalcremer),
    path('openapi', get_schema_view(
        title="Web Scraping",
        description="Web Scraping para capturar informações de produtos",
        version="0.1.0"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='openapi.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='openapi')
]

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT, show_indexes=True)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT, show_indexes=True)
