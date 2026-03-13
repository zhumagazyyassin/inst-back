from rest_framework import serializers
from .models import User, Post, Media, Comment, Like, Follow

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'avatar_url']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'url', 'order_idx']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_name', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    post_caption = serializers.ReadOnlyField(source='post.caption')
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_name', 'post', 'post_caption']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    media = MediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'caption', 'media', 'comments', 'likes_count', 'is_liked', 'created_at']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.ReadOnlyField(source='follower.username')
    following_name = serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_name', 'following', 'following_name']