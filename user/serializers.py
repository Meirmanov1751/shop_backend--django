from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from general.serializers import MediaFileSerializer
from user.models import User
from utils.validate_phone import validate_phone


class LoginSerializer(Serializer):
    def validate(self, data):
        data['phone'] = validate_phone(data['phone'])
        return data

    phone = serializers.CharField()
    role = serializers.CharField(default=User.ROLES.USER)

class CheckCodeSerializer(LoginSerializer):
    code = serializers.CharField(required=True)


class UserSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if hasattr(instance, 'avatar'):
            avatar = instance.avatar
        elif 'avatar' in instance:
            avatar = instance['avatar']
        if avatar:
            response['avatar'] = MediaFileSerializer(avatar, context=self.context).data
        else:
            response['avatar'] = None
        return response
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(ModelSerializer):


    class Meta:
        model = User
        fields = ['fullname', 'avatar', 'email']
