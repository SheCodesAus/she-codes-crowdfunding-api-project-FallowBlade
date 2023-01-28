from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics, permissions
from rest_framework import filters

from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, ProjectSearch

from .permissions import IsOwnerReadOnly, IsSupportReadOnly

# the "." means "from" so from the models file, import Project.
# Get = get something
# Post = create
# serializers need to be told to do many
# return Response(serializer.data) = we are getting te data from the serializer
# self = defining it as a class
# # Views, in the most simplest terms, is just something that will be used to interact with the backend and helps structure your code.
#

# With the below class, you will be repeating this for different views. The only thing you are really changing is the avatar(generic) naming convention. So in the below class ProjectList(APIView), the ONLY convention you are changing is the word "Project", "projects". For instance, you would swap this to be "Pledge" for others.



class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        seriaizer = ProjectSerializer(projects, many=True)
        return Response(seriaizer.data)
    # GET the projects

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #add new Porject, if not valid, don't save.

# get the data from the request, serialize it, then
# if the serializer is valid, save it.

class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerReadOnly
    ]

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

# Update a project
    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #  This DELETE Function Works - WOOP, do I need to add CASCADE is my question..?
    def delete(self,request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ProjectSearch = attempt to make projects searchable by title
class SearchAPIView(generics.ListCreateAPIView):
        queryset = Project.objects.all()
        serializer_class = ProjectSearch
        search_fields = ['title', 'description',]
        filter_backends = (filters.SearchFilter,)

    
class PledgeList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the pledges
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Pledge.objects.filter(supporter=user)
    
# class PledgeDetailView(generics.RetrieveUpdateAPIView)

class PledgeDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSupportReadOnly
    ]
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

#   def get_object(self, pk):
#         try:
#             pledge = Pledge.objects.get(pk=pk)
#             self.check_object_permissions(self.request, pledge)
#             return pledge
#         except Pledge.DoesNotExist:
#             raise Http404
    
# def get(self, request, pk):
#         pledge = self.get_object(pk)
#         serializer = PledgeDetailView(pledge)
#         return Response(serializer.data)
    
# def put(self, request, pk):
#         pledge = self.get_object(pk)
#         data = request.data
#         serializer = PledgeSerializer(
#             instance=pledge,
#             data=data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     #  This DELETE Function Works - WOOP, do I need to add CASCADE is my question..?
# def delete(self,request,pk):
#         pledge = self.get_object(pk)
#         serializer = PledgeDetailView(pledge)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=204)
    
# pk=pk means the primary key is equal to the value given.  
# we will re-use the def get_object code accross many places to save us doing it again.