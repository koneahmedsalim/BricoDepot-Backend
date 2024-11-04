# bricodepot/serializers.py

from rest_framework import serializers
from .models import CustomUser, Post, Comment, Follow, Notification, PrivateMessage

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','password' ,'profile_picture', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']

class FollowSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(read_only=True)
    followed = CustomUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'created_at', 'is_read']

class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'recipient', 'content', 'sent_at', 'is_read']
