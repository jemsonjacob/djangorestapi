from rest_framework.serializers import ModelSerializer
from book.models import Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework import serializers



class BookSerializer(ModelSerializer):
    class Meta:
       model=Book
       fields = ['book_name','author']

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ["username","email","password"]
    def create(self,validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'])

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()



