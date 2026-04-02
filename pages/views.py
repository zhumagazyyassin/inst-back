from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, Follow, Media, Story, Note
from .serializers import *

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        # Постты сақтаймыз
        post = serializer.save(author=self.request.user if self.request.user.is_authenticated else User.objects.first())
        # Суретті Media кестесіне автоматты тіркеу
        file_data = self.request.FILES.get('image') or self.request.FILES.get('file')
        if file_data:
            Media.objects.create(post=post, file=file_data, file_type='image')

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else User.objects.first())

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else User.objects.first())

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

class FollowToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        if request.user == user_to_follow: return Response({"error": "Self-follow"}, status=400)
        follow_obj = Follow.objects.filter(follower=request.user, following=user_to_follow)
        if follow_obj.exists():
            follow_obj.delete()
            return Response({"message": "Unfollowed"})
        Follow.objects.create(follower=request.user, following=user_to_follow)
        return Response({"message": "Followed"})