from rest_framework import serializers

from posts.models import Post, Comment, Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'post', 'created')
        fields = ['id', 'author', 'post', 'text', 'created']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'group', 'pub_date']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']
