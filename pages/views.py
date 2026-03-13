from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like, Follow, User
from .serializers import PostSerializer, LikeSerializer, FollowSerializer, UserSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeListView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like_queryset = Like.objects.filter(user=request.user, post=post)
        if like_queryset.exists():
            like_queryset.delete()
            return Response({"message": "Unliked", "is_liked": False}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Liked", "is_liked": True}, status=status.HTTP_201_CREATED)

class FollowListCreateView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)