from rest_framework import serializers
from .models import Post, Comment, Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ('post', 'author')
        fields = ['id', 'author', 'post', 'text', 'created']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, required=False, read_only=True)
    group = serializers.SlugRelatedField(slug_field='id',
            queryset=Group.objects.all(), required=False, allow_null=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'group', 'pub_date']