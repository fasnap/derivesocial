
from post.models import Comment, Post
from rest_framework import serializers
from user_app.api.serializers import AccountSerializer

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post']
        
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    likes = AccountSerializer(many=True,read_only=True)
    class Meta:
        model=Post
        fields = [
            "id",
            "title",
            "description",
            "post_image",
            "author",
            "comments",
            "total_likes",
            "likes",
        ]
    def get_total_likes(self,instance):
        return instance.likes.count()
       



























       
    # @staticmethod
    # def get_likes_amount(obj):
    #     return obj.likes.count()

    # @staticmethod
    # def get_comments_amount(obj):
    #     return obj.comments.count()

    # def get_is_liked(self, obj):
    #     user = self.context['request'].user
    #     print (user)
    #     if user and not user.is_anonymous:
    #         return bool(obj.likes.filter(author=user))
    #     return None
# class LikesDetailedSerializer(serializers.ModelSerializer):
#     author = AccountSerializer(read_only=True)
#     post = PostSerializer(read_only=True)

#     class Meta:
#         model = Like
#         fields = "__all__"
#         extra_kwargs = {"author": {"read_only": True}}
       
        # read_only_fields = ['user']
# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=4000)
#     post_image=serializers.ImageField()
#     author_id = serializers.IntegerField()
#     post_date=serializers.DateField()

#     def create(self, validated_data):
#         return Post.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.author_id = validated_data.get('author_id', instance.author_id)
#         instance.post_image=validated_data.get('post_image', instance.post_image)
#         instance.post_date = validated_data.get('post_date', instance.post_date)
#         instance.save()
#         return instance
    