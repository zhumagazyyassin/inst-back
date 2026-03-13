from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User, Post, Like, Comment, Follow, Media
from .serializers import PostSerializer, UserSerializer, CommentSerializer, MediaSerializer

# --- USERS ---
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# --- POSTS ---
class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

# --- ACTIONS ---
class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Лайк алынды"}, status=status.HTTP_200_OK)
        return Response({"message": "Лайк басылды"}, status=status.HTTP_201_CREATED)

class PostLikesListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(like__post_id=self.kwargs['pk'])

# --- COMMENTS ---
class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])
    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

# --- MEDIA ---
class MediaCreateView(generics.ListCreateAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Media.objects.filter(post_id=self.kwargs['pk'])
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(post=post)

class MediaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Media.objects.filter(post_id=self.kwargs['post_id'])
    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

# --- FOLLOW ---
class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        is_following = Follow.objects.filter(follower=request.user, followee=target).exists()
        return Response({"is_following": is_following})
    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        if target == request.user: return Response({"error": "Self-follow"}, status=400)
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=target)
        if not created: follow.delete(); return Response({"message": "Unfollowed"})
        return Response({"message": "Followed"})

class UserFollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(following__followee_id=self.kwargs['pk'])

class UserFollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(followers__follower_id=self.kwargs['pk'])

# --- AUTH & PROFILE ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Тіркелу үшін рұқсат керек емес

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self): return self.request.user

class UserProfileDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self): return self.request.user