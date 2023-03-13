from django.shortcuts import render
from rest_framework.views import APIView
from unicodedata import category
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import Project, Pledge, Category
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, ProjectSearch, CategoryDetailSerializer, CategorySerializer

from .permissions import IsOwnerReadOnly, IsSupportReadOnly


# the "." means "from" so from the models file, import Project.

# return Response(serializer.data) = we are getting te data from the serializer
# self = defining it as a class
# So in the below class ProjectList(APIView), the ONLY convention you are changing is the word "Project", "projects". For instance, you would swap this to be "Pledge" for others.


# class ProjectList(APIView):
    
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
#     # GET the projects

#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #add new Porject, if not valid, don't save.

# get the data from the request, serialize it, then
# if the serializer is valid, save it.


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["owner", "is_open"]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    #  This DELETE Function Works - WOOP, do I need to add CASCADE is my question..?
    def delete(self,request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchAPIView(generics.ListCreateAPIView):
        queryset = Project.objects.all()
        serializer_class = ProjectSearch
        search_fields = ['title', 'description', 'owner__username']
        filter_backends = (filters.SearchFilter,)
        # This means set the query to capture all Project fields from the project, call the ProjectSearch serializer (with the rules in-built) and then query 'title' and 'project' fields for the requested string.
         # Note that this is currently not able to be customisable to extent of "containts, doesnotcontain, rules etc."

class PledgeList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["supporter"]

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)
# this means, create a pledge based on the pledgeserializer, and save this to the list as being created by the user)
 
    # def get_queryset(self):
    #     user = self.request.user
    #     return Pledge.objects.filter(supporter=user)
# this means that ONLY pledges the created by the user appear in the list.

class PledgeDetailView(generics.RetrieveUpdateDestroyAPIView):
# allows only the pledge creator(owner) to update or destroy their pledge.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSupportReadOnly
    ]
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
# Get all category objects and create a list of these for the view.

class CategoryDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request,category)
            return category
            
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        data = request.data
        serializer = CategoryDetailSerializer(
            instance=category,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# pk=pk means the primary key is equal to the value given.  
# we will re-use the def get_object code accross many places to save us doing it again.