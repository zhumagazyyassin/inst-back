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
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_name', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    media = MediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'caption', 'media', 'comments', 'likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.post_likes.count() # Like моделіндегі related_name-ге байланысты

class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.ReadOnlyField(source='follower.username')
    following_name = serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = Follow
        fields = '__all__'