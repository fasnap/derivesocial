
from django.urls import path
from rest_framework import views
from .views import AddLikeUnlikeView, CommentDetail, PostDetailAV,PostListAV,CommentList

urlpatterns = [
    path('posts/', PostListAV.as_view()),
    path('<int:pk>/',PostDetailAV.as_view(),name='post-detail'),  
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('like/unlike/<int:post_id>/', AddLikeUnlikeView.as_view(), name='like_unlike')
]