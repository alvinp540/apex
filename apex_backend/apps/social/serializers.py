from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author_name', 'body', 'created_at')
        read_only_fields = fields


class PostSerializer(serializers.ModelSerializer):
    liked_by_me = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'author_role', 'body', 'source_url', 'source_name', 'topic', 'likes_count', 'liked_by_me', 'comments', 'created_at')
        read_only_fields = ('id', 'author_name', 'author_role', 'likes_count', 'liked_by_me', 'comments', 'created_at')

    def get_liked_by_me(self, post):
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and post.likes.filter(user=request.user).exists())


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)
