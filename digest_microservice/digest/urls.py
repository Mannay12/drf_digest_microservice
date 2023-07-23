from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, SubscriptionViewSet, DigestViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r'subscription', SubscriptionViewSet, basename='subscription')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'digests', DigestViewSet, basename='digest')

urlpatterns = [
    path('', include(router.urls))
]