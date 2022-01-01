from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from post.api.serializers import  PostSerializer
from post.models import Comment, Post
from rest_framework import generics, serializers
from rest_framework import permissions
from rest_framework.response import Response
from post.api.permissions import OwnerOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          OwnerOnly,]

class AddLikeUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        if post.likes.filter(pUnablek=request.user.pk).exists():
            post.likes.remove(request.user)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            post.likes.add(request.user)
            return Response(status=status.HTTP_200_OK)

class PostListAV(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(OwnerOnly,permissions.IsAuthenticated,)
    serializer_class=PostSerializer
    queryset=Post.objects.all()
   
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

# class CommentViewSet(ModelViewSet):
    # authentication_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly, UpdateOwn]
    # serializer_class = CommentSerializer
    # queryset = Comment.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


# class LikeViewSet(ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # serializer_class = LikesSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ("author__id",)
    # queryset = Like.objects.all()

    # def create(self, request, *args, **kwargs):
    #     post_id = request.data["post"]
    #     post = generics.get_object_or_404(Post, pk=post_id)
    #     new_like, _ = Like.objects.get_or_create(author=request.user, post=post)
    #     serializer = self.serializer_class(new_like).data
    #     return Response(data=serializer, status=status.HTTP_201_CREATED)


# class LikedApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # serializer_class = PostSerializer

    # def get(self, request):
    #     liked_posts = Post.objects.filter(likes__author__id=request.user.id)
    #     serializer_data = self.serializer_class(
    #         liked_posts, many=True, context={"request": request}
    #     ).data

    #     return Response(data=serializer_data)


# class PostLikes(APIView):
    # authentication_classes = [TokenAuthentication]
    # serializer_class = LikesSerializer

    # def get(self, request, post_id):
    #     post = get_object_or_404(Post, pk=post_id)
    #     post_data = PostSerializer(post, context={"request": request}).data
    #     likes_data = self.serializer_class(
    #         post.likes, many=True, context={"request": request}
    #     ).data

    #     return Response(data={"likes": likes_data, "is_liked": post_data["is_liked"]})


# class PostComments(APIView):
    # authentication_classes = [TokenAuthentication]
    # serializer_class = CommentSerializer

    # def get(self, request, post_id):
    #     post = get_object_or_404(Post, pk=post_id)
    #     comments_data = self.serializer_class(
    #         post.comments, many=True, context={"request": request}
    #     ).data

    #     return Response(data=comments_data)


    # def perform_create(self,serializer):
    #     return serializer.save(author=self.request.user)
    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)
# class PostDetailAV(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get(self,request,pk):
#         try:
#             posts=Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             return Response({'error':'Post not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=PostSerializer(posts)
#         return Response(serializer.data)
#     def put(self,request,pk):
#         posts=Post.objects.get(pk=pk)
#         serializer=PostSerializer(posts,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         post=Post.objects.get(pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class PostView(APIView):
#     def get(self, request, pk=None):
#         if pk:
#             post = get_object_or_404(Post.objects.all(), pk=pk)
#             serializer = PostSerializer(post)
#             return Response({"post": serializer.data})
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response({"post": serializer.data})

    # def post(self, request):
    #     post = request.data.get('post')

    #     # Create an post from the above data
    #     serializer = PostSerializer(data=post)
    #     if serializer.is_valid(raise_exception=True):
    #         post_saved = serializer.save()
    #     return Response({"success": "post '{}' created successfully".format(post_saved.title)})

    # def post(self,request):
    #     post = request.data

    #     serializer = PostSerializer(data=post)
    #     if serializer.is_valid(raise_exception=True):
    #         post_saved=serializer.save()

    #     return Response({"success":"post '{}' created successfully".format(post_saved.title)})

    # def put(self, request, pk):
    #     saved_post = get_object_or_404(Post.objects.all(), pk=pk)
    #     data = request.data.get('post')
    #     serializer = PostSerializer(instance=saved_post, data=data, many=True)

    #     if serializer.is_valid(raise_exception=True):
    #         post_saved = serializer.save()
    #     return Response({"success": "post '{}' updated successfully".format(post_saved.title)})


    # def delete(self, request, pk):
    #     # Get object with this pk
    #     post = get_object_or_404(Post.objects.all(), pk=pk)
    #     post.delete()
    #     return Response({"message": "post with id `{}` has been deleted.".format(pk)},status=204)


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def create(self, request):
#         serializer = PostSerializer(
#             data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True) # check all fields is valid before attempting to save
#         serializer.save(user=request.user)
#         return Response(serializer.data)


# class PostListAV(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     permission_classes = (
#         IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

# class PostListAV(generics.ListCreateAPIView):
#     parser_classes = (MultiPartParser, FormParser)
#     # permission_classes = (
#     #     IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
#     def get(self,request):
#         posts=Post.objects.all()
#         serializer=PostSerializer(posts,many=True)
#         return Response(serializer.data)
#     def post(self,request,pk):
#         serializer=PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class ProductListAV(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [IsAdminOrReadOnly]
#     def get(self,request):
#         products=Product.objects.all()
#         serializer=ProductSerializer(products,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)