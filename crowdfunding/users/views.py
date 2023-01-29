from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer


class CustomUserList(APIView):
    
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

# This updates/edits a users details (incl. password - I think!):
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

# class ChangePasswordView(generics.UpdateAPIView):
#         model = CustomUser
#         permission_classess = (IsAuthenticated)

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj
        
#         def update(self,request, *args, **kwargs):
#             self.object = self.get_serializer(data=request.data)
#             serializer = ChangePasswordSerializer

#             if serializer.is_valid():
#                 # check old password
#                 if not self.object.check_password(serializer.data.get("old_password")):
#                          return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                 # set_password also hashes the password that the user will get
#                 self.object.set_password(serializer.data.get("new_password"))
#                 self.object.save()
#                 response = {
#                     'status': 'success',
#                     'code': status.HTTP_200_OK,
#                     'message': 'Password updated successfully',
#                     'data': []
#                 }

#                 return Response(response)

#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

