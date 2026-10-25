from django.urls import path

from users import views

urlpatterns = [
    path('users', views.UserCreate.as_view()),
]
