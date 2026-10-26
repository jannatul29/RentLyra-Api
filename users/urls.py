from django.urls import path

from users import views

urlpatterns = [
    path('users', views.UserCreate.as_view()),
    path('users/activate', views.UserActivate.as_view()),
    path('users/authentication', views.LoginAPIView.as_view()),
]
