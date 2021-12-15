from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from reporting.serializers import UserCreationSerializer, LoginSerializer


class UserCreationView(generics.GenericAPIView, mixins.CreateModelMixin):
    model = User
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SignInView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                token,created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'login fail'}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response(serializer.errors)
