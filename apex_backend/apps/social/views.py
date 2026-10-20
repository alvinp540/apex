from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, PostLike
from .serializers import CommentCreateSerializer, PostSerializer


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.prefetch_related('comments__author', 'likes')[:50]
        return Response(PostSerializer(posts, many=True, context={'request': request}).data)

    def post(self, request):
        body = str(request.data.get('body', '')).strip()
        if not body:
            return Response({'body': 'Write something first.'}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(author=request.user, author_name=request.user.username, author_role=request.user.role, body=body, topic='Community')
        return Response(PostSerializer(post, context={'request': request}).data, status=status.HTTP_201_CREATED)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        post.likes_count = post.likes.count()
        post.save(update_fields=['likes_count'])
        return Response({'liked_by_me': created, 'likes_count': post.likes_count})


class PostCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(post=post, author=request.user)
        return Response({'author_name': request.user.username, 'body': comment.body, 'created_at': comment.created_at}, status=status.HTTP_201_CREATED)
