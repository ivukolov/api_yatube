from rest_framework import serializers
from .models import Post, Comment, Group


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['author', 'post', 'text']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['text', 'author', 'image', 'group', 'comments']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'