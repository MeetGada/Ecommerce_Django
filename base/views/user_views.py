from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.models import User
from base.serializers import UserSerializer, UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['name'] = user.first_name
        token['isAdmin'] = user.is_staff
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterUserView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)
        data = request.data
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        if data['password'] != '':
            user.password = make_password(data['password'])
        user.save()
        return Response(serializer.data)

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            data = request.data
            user.first_name = data['name']
            user.username = data['email']
            user.email = data['email']
            user.is_staff = data.get('isAdmin', user.is_staff)
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            userForDeletion = User.objects.get(id=pk)
            userForDeletion.delete()
            return Response('User was deleted')
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
