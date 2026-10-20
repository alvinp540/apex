from django.urls import path
from .views import PostCommentView, PostLikeView, PostListView

urlpatterns = [
    path('posts/', PostListView.as_view()),
    path('posts/<uuid:post_id>/like/', PostLikeView.as_view()),
    path('posts/<uuid:post_id>/comments/', PostCommentView.as_view()),
]
