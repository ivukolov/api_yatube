from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import PostViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)



urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
