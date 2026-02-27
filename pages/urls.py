from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PostListAPIView, UserListAPIView, PostDetailAPIView, 
    UserDetailAPIView, RegisterView, UserProfileUpdateView, 
    UserProfileDeleteView, PostLikeView, PostLikesListView, 
    CommentCreateView, CommentDetailView, UserFollowView, 
    UserFollowersListView, UserFollowingListView,
    MediaCreateView, MediaDetailView
)

urlpatterns = [
    # AUTH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    
    # PROFILE
    path('api/profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('api/profile/delete/', UserProfileDeleteView.as_view(), name='profile-delete'),
    
    # POSTS
    path('api/posts/', PostListAPIView.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('api/posts/<int:pk>/likes-list/', PostLikesListView.as_view(), name='post-likes-list'),
    
    # COMMENTS
    path('api/posts/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment-create'),
    path('api/posts/<int:post_id>/comment/<int:pk>/', CommentDetailView.as_view(), name='post-comment-detail'),

    # MEDIA
    path('api/posts/<int:pk>/media/', MediaCreateView.as_view(), name='post-media-create'),
    path('api/posts/<int:post_id>/media/<int:pk>/', MediaDetailView.as_view(), name='post-media-detail'),

    # USERS & FOLLOW
    path('api/users/', UserListAPIView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/follow/', UserFollowView.as_view(), name='user-follow'),
    path('api/users/<int:pk>/followers/', UserFollowersListView.as_view(), name='user-followers'),
    path('api/users/<int:pk>/following/', UserFollowingListView.as_view(), name='user-following'),
]