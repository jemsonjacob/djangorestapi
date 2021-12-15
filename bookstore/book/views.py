from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from book.models import Book
from book.serializers import BookSerializer, UserCreationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from book.serializers import LoginSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


# Create your views here.
class BookList(APIView):
    model = Book
    serializer_class = BookSerializer

    def get(self, request):
        books = self.model.objects.all()
        serializer = self.serializer_class(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetails(APIView):
    model = Book
    serializer_class = BookSerializer

    def get_object(self, id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        book = self.model.objects.get(kwargs['id'])
        serializer = self.serializer_class(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        book = self.get_object(kwargs['id'])
        serializer = self.serializer_class(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        book = self.get_object(kwargs['id'])
        book.delete()
        return Response(status=status.HTTP_200_OK)


class BookMixinList(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    model = Book
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookDetailMixins(generics.GenericAPIView,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    model = Book
    serializer_class = BookSerializer
    queryset = model.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UserCreationView(generics.GenericAPIView,
                       mixins.CreateModelMixin):
    model = User
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class SignInView(APIView):
    serializer_class=LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)

                return Response({'token':token.key},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'login fail'},status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response(serializer.errors)

