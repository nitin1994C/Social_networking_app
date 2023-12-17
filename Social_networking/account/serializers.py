
from rest_framework import serializers
from .models import User, UserProfile  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'user', 'name','friends', 'profile_picture', 'cover_photo', 'gender',
            'phone_no', 'address_line_1', 'address_line_2', 'country', 'city',
            'pincode', 'created_at', 'modified_at'
        )
    
