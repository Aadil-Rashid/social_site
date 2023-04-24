from rest_framework import serializers

from users.models import CustomUser
from users.models import Friendship

from users.commons import valid_email


class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email')


class FriendshipSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = Friendship
        fields = ('user_id', 'name', 'email')
        
    def get_user_id(self, obj):
        return obj.sender.id
    
    def get_name(self, obj):
        return obj.sender.name
        
    def get_email(self, obj):
        return obj.sender.email
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', "name", 'email', 'password')
        extra_kwargs = {'password':{'write_only': True}}
    
    def validate(self, data):
        if not valid_email(data.get('email')):
            raise serializers.ValidationError('Invalid email address')
        if len(data.get('password')) < 4:
            raise serializers.ValidationError('Password length should be atleast 4 digit long')
        if not (data.get('name')):
            raise serializers.ValidationError('name is missing')
        return data
    
    def create(self, validated_data):      
        user = CustomUser.objects.create_user(
                    validated_data['email'], validated_data['password'], name=validated_data['name'])
        return user
               
 