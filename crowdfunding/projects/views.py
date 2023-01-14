from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from .models import Project
from .serializers import ProjectSerializer

# the "." means "from" so from the models file, import Project.
# Get = get something
# Post = create
# D.
# serializers need to be told to do many
# return Response(serializer.data) = we are getting te data from the serializer
# self = defining it as a class


class ProjectList(APIView):

    def get(self, request):
        projects = Project.objects.all()
        seriaizer = ProjectSerializer(projects, many=True)
        return Response(seriaizer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get the data from the request, serialize it, then
# if the serializer is valid, save it.

class ProjectDetail(APIView):

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    

# pk=pk means the primary key is equal to the value given.  
# we will re-use the def get_object code accross many places to save us doing it again.

