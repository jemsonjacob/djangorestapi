from rest_framework.serializers import ModelSerializer
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework import serializers



class TodoSeralizer(ModelSerializer):
    class Meta:
        model = Todo
        fields=['task_name','completed','user']

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields=['username','email','password']

    def create(self,validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'])



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
