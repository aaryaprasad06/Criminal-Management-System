from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

#swagger setup
schema_view = get_schema_view(
    openapi.Info(
        title="Criminal Management API",
        default_version='v1',
        description="API documentation for the Criminal Management System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
router = DefaultRouter()
router.register(r'criminals', views.CriminalViewSet)
router.register(r'crimes', views.CrimeViewSet)
router.register(r'arrests', views.ArrestViewSet)
router.register(r'casefiles', views.CaseFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]