from rest_framework import serializers
from .models import User, Post, Media, Comment, Like, Follow

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'bio', 'avatar_url']

    def create(self, validated_data):
        # Парольді хэштеп сақтау үшін .create_user міндетті!
        user = User.objects.create_user(**validated_data)
        return user

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file_url', 'file_type']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'caption', 'media', 'likes_count', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'