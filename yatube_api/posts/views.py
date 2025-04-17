from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_update(instance)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments_list(self, request, pk=None):
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                post = get_object_or_404(Post, pk=pk)
                serializer.save(author=self.request.user, post=post)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        comment = Comment.objects.filter(post=pk).all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=['get', 'put', 'patch', 'delete'],
            url_path='comments/(?P<comment_pk>[^/.]+)'
            )
    def comment_detail(self, request, pk=None, comment_pk=None):
        comment = get_object_or_404(Comment, post=pk, pk=comment_pk)

        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            if request.user != comment.author:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            serializer = CommentSerializer(
                comment,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if request.user != comment.author:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer