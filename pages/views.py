from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like_queryset = Like.objects.filter(user=request.user, post=post)
        if like_queryset.exists():
            like_queryset.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        Like.objects.create(user=request.user, post=post)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)