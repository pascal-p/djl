from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

# Create your views here.
from .models import Post
from .permissions import IsAuthorOrReadOnly, AuthIsAdminOrReadOnly
from .serializers import PostSerializer, UserSerializer

# class ReadOnly(permissions.BasePermission):
#    def has_permission(self, request, view):
#        return request.method in permissions.SAFE_METHODS

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthIsAdminOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
