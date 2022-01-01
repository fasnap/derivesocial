from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_app.api.permissions import IsOwnerOrReadOnly
from user_app.api.serializers import AccountSerializer, ChangePasswordSerializer, ProfileSerializer,UserRegistrationSerializer, UserSerializer
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from user_app.models import Account, Profile
from rest_framework.decorators import api_view
from user_app.api.permissions import IsObjectOwner
class user_registration_view(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['fullname'] = self.user.fullname
        data['email'] = self.user.email
        data['phone'] = self.user.phone
        data['id']=self.user.id
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset=Account.objects.all()
    permission_classes=[IsAuthenticated,IsObjectOwner,]
    serializer_class = ChangePasswordSerializer

class UserSearchListView(generics.ListAPIView):
    queryset=Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends=(filters.DjangoFilterBackend, SearchFilter,)
    filter_fields = ('username',)
    search_fields=('fullname',)

# class AccountViewSet(viewsets.ModelViewSet):
#     queryset=Account.objects.all()
#     serializer_class = AccountSerializer
#     filter_backends=(filters.DjangoFilterBackend,SearchFilter)
#     filter_fields=('username',)
#     search_fields=('fullname',)

# class UserSearchListView(viewsets.ViewSet):
#     def list(self, request, username):
#         accounts = Account.objects.filter(username__username=username)
#         accounts_to_return = AccountSerializer(accounts, many=True).data

#         return Response(accounts_to_return)

# class UserProfileViewSet(ModelViewSet):
#     queryset = UserProfile.objects.all()
    # authentication_classes = [TokenAuthentication]
    # serializer_class = UserProfileSerializer
    # permission_classes = [UpdateOwnProfile]


# class UserProfileView(generics.RetrieveAPIView):

#     # permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         try:
#             user_profile = UserProfile.objects.get(user=request.user)
#             status_code = status.HTTP_200_OK
#             response = {
#                 'success': 'true',
#                 'status code': status_code,
#                 'message': 'User profile fetched successfully',
#                 'data': [{
#                     'fullname': user_profile.fullname,
#                     'phone': user_profile.phone,
#                     'age': user_profile.age,
#                     'bio': user_profile.bio,
#                     'profile_picture': user_profile.bio,
#                     }]
#                 }

#         except Exception as e:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': 'false',
#                 'status code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'User does not exists',
#                 'error': str(e)
#                 }
#         return Response(response, status=status_code)


# class TokenObtainPairView(APIView):
#     def post(self, request, format=None):
#         token_user_email = request.user.email
#         token_user_username = request.user.username
#         pass
    

# class APILogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         if self.request.data.get('all'):
#             token: OutstandingToken
#             for token in OutstandingToken.objects.filter(user=request.user):
#                 _, _ = BlacklistedToken.objects.get_or_create(token=token)
#             return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
#         refresh_token = self.request.data.get('refresh_token')
#         token = RefreshToken(token=refresh_token)
#         token.blacklist()
#         return Response({"status": "OK, goodbye"})
# from user_app.api.serializers import UserRegistrationSerializer
# from rest_framework.response import Response 
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import api_view

# @api_view(['POST',])
# def user_registration_view(request):

#     if request.method == 'POST':
#         serializer = UserRegistrationSerializer(data=request.data)

#         data = {}

#         if serializer.is_valid():
#             account = serializer.save()

#             data['response'] = 'Registration successful'
#             data['username'] = account.username
#             data['email'] = account.email
#             data['fullname'] = account.fullname
#             data['phone'] = account.phone
            
#             refresh = RefreshToken.for_user(account)
#             data['token'] = {
#                 'refresh': str(refresh),
#                 'access':str(refresh.access_token),
#             }

#         else:
#             data = serializer.errors
        
        
#         return Response(data)
