from django.db import models
import uuid
from apps.accounts.models import User


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_posts', null=True, blank=True)
    author_name = models.CharField(max_length=120, default='Apex Field Notes')
    author_role = models.CharField(max_length=120, default='Capability research')
    body = models.TextField()
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=120, blank=True)
    topic = models.CharField(max_length=80, default='Capability')
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)
        db_table = 'social_posts'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_likes')

    class Meta:
        constraints = [models.UniqueConstraint(fields=('post', 'user'), name='unique_social_post_like')]


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_comments')
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'social_comments'
