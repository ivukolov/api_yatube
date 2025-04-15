from rest_framework import serializers
from .models import Post, Comment, Group


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['author', 'post', 'text']


class GroupSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField()
    class Meta:
        model = Group
        fields = ['title', 'slug', 'description', 'posts']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    group = GroupSerializer(many=True)

    class Meta:
        model = Post
        fields = ['text', 'author', 'image', 'group', 'comments']

