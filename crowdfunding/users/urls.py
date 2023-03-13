from django.urls import path
from users.views import ChangePasswordView

from . import views

urlpatterns = [
    path('', views.CustomUserList.as_view(), name='customuser-list'),
    path('<int:pk>', views.CustomUserDetail.as_view(), name='customeruser-detail'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_password_change'),
]