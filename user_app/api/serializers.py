from user_app.models import Account, Profile
from rest_framework import serializers

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 =serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=Account
        fields=('old_password','password','password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password not match"})
        return attrs
    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"old password is incorrect"})
        return value
    def update(self,instance,validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']

class ProfileSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=Profile
        fields='__all__'
  
    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     date_of_birth = validated_data.pop('date_of_birth')
    #     username = self.data['user']['username']
    #     user = Account.objects.get(username=username)
    #     print(user)
    #     user_serializer = UserSerializer(data=user_data)
    #     if user_serializer.is_valid():
    #         user_serializer.update(user, user_data)
    #     instance.save()
    #     return instance
class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Account
        fields = ['fullname','username','profile']

    def update(self, instance, validated_data):
        # We try to get profile data
        profile_data = validated_data.pop('profile', None)
        # If we have one
        if profile_data is not None:
            # We set address, assuming that you always set address
            # if you provide profile
            instance.profile.date_of_birth = profile_data['date_of_birth']
            instance.profile.photo = profile_data['photo']
            # And save profile
            instance.profile.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    # profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['fullname',  'email', 'username', 'phone', 'password', 'password2']
        
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data.get('email')
        phone = self.validated_data.get('phone')
        
        if password != password2 :
            raise serializers.ValidationError({'error':'Password should be the same'})
        if email:
            if Account.objects.filter(email=self.validated_data['email']).exists():
                raise serializers.ValidationError({'error':'Email id already exists'})
        elif phone:
            if Account.objects.filter(phone=self.validated_data['phone']).exists():
                raise serializers.ValidationError({'error':'phone already exists'})
        else:
            raise serializers.ValidationError({'error':'phone or email is required'})
        account = Account(
            fullname=self.validated_data['fullname'],
            username = self.validated_data['username'],
            email = self.validated_data.get('email'),
            phone = self.validated_data.get('phone')
            )
        account.set_password(password)
        account.save()

        return account

class AccountSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ('email','phone','username','posts','comments')



# class UserProfileSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     follows = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=UserProfile.objects.all())
#     followed_by = serializers.PrimaryKeyRelatedField(
#         many=True, read_only=True)
#     profile_id = serializers.IntegerField(source="id")

#     class Meta:
#         model = UserProfile
#         fields = ["profile_id", "user", "age", "photo",
#                   "description", "follows", "followed_by"]

#         extra_kwargs = {
#             "followed_by": {
#                 "read_only": True,
#             }
#         }
