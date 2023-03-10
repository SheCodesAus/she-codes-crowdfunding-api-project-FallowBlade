from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer


class CustomUserList(APIView):

    # This class is returning a list of users and an ability to post a new user with the required serializer pieces.
    
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CustomUserDetail(APIView):

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    # def create(self,request,pk):
    #     user = self.create.__new__(pk)
    #     serializer = CustomUserSerializer
    #     return Response(serializer.data)

# This updates/edits a users details:
    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CreateUser(generics.CreateAPIView):
    
    def create(self,request,pk):
        queryset = CustomUser.objects.all
        serializer = CustomUserSerializer
        return Response(serializer.data)

class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


