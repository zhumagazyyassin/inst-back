from django.urls import path
from .views import (
    RegisterView, UserListAPIView, UserDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, LikeToggleView
)

urlpatterns = [
    # --- USERS ---
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # --- POSTS ---
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # --- ACTIONS (Comments & Likes) ---
    path('posts/<int:pk>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='post-like'),
]