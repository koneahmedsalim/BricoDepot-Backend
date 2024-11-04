from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import CustomUser, Post, Comment, Follow, Notification, PrivateMessage
from .serializers import (
    CustomUserSerializer, PostSerializer, CommentSerializer,
    FollowSerializer, NotificationSerializer, PrivateMessageSerializer
)
from .permissions import IsOwnerOrReadOnly

# View for Users (Read Only)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# View for Posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# View for Comments
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# View for Follows
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

# View for Notifications (Read Only)
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter to return only the notifications of the current user
        return Notification.objects.filter(recipient=self.request.user)

# Registration View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for Private Messages
class PrivateMessageViewSet(viewsets.ModelViewSet):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(sender=user) | PrivateMessage.objects.filter(recipient=user)

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is inactive"}, status=status.HTTP_403_FORBIDDEN)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def test_token(request):
    return Response({})

@api_view(['POST'])
def login(request):
    return Response({})