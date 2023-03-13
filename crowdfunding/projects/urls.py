from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# path in Url_patterns is a function

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name="project-list"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('pledges/', views.PledgeList.as_view(), name="pledge-list"),
    path('pledges/<int:pk>/', views.PledgeDetailView.as_view(), name="pledge-view"),
    path('search/', views.SearchAPIView.as_view(), name="project-search"),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name='category'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


# format suffix patterns takes all your urls and helps you to tell them to become something else, like JSON.

