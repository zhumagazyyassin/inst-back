from django.contrib import admin
from .models import User, Post, Media, Comment, Like, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Media)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)