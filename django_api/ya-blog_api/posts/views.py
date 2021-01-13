from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response


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

    def create(self, request):
        "set author, validate, save and serialize"
        data = request.data
        data['author'] = request.user.id
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        post = Post.objects.get(id=pk)
        print(f"==> get post: {post} / author: {post.author}")
        print(f"==> get current user: {request.user} / id: {request.user.id}")

        if post.author == request.user:
            serializer = PostSerializer(instance=post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response('Permission Denied', status=status.HTTP_403_FORBIDDEN)



class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthIsAdminOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
