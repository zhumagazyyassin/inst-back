from django.contrib import admin
from .models import User, Post, Media, Follow, Comment, Like

@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 'title'-ды 'caption'-ға ауыстырдық, өйткені модельде қазір солай
    list_display = ('id', 'author', 'caption', 'created_at')

# Қалғандарын қарапайым тіркей саламыз
admin.site.register(Media)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)