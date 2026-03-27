from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserViewSet, PostViewSet, 
    CommentViewSet, LikeToggleView, FollowToggleView
)

router = DefaultRouter()
router.register(r'users', UserViewSet) # api/users/
router.register(r'posts', PostViewSet) # api/posts/
router.register(r'comments', CommentViewSet) # api/comments/

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('users/<int:user_id>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
]