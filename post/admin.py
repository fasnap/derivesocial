from django.contrib import admin
from post.models import Comment, Post
admin.site.register(Post)
# admin.site.register(Like)
admin.site.register(Comment)