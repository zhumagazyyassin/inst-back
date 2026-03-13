from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    LikeToggleView,
    FollowListCreateView, FollowDetailView
)

urlpatterns = [
    # Users
    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    
    # Posts
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    
    # Comments
    path('comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
    
    # Likes (Посттың ID-і арқылы)
    path('posts/<int:pk>/like/', LikeToggleView.as_view()),
    
    # Follows
    path('follows/', FollowListCreateView.as_view()),
    path('follows/<int:pk>/', FollowDetailView.as_view()),
]