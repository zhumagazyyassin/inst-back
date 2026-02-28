from django.contrib import admin
from .models import User, Post, Media, Follow, Comment, Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Media)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)