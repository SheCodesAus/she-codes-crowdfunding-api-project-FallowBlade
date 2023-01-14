from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# path in Url_patterns is a function

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name="project-list"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# format suffix patterns takes all your urls and helps you to tell it to become something else, like JSON.

