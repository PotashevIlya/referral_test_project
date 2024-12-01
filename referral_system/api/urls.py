from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, get_token, signup

auth_urls = [
    path('auth/signup', signup),
    path('auth/get_token', get_token)
]

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(auth_urls)),
    path('', include(router.urls))
]
