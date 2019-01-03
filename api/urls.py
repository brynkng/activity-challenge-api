from django.urls import path

from . import views

urlpatterns = [
    path('competitions/', views.CompetitionListCreate.as_view(), name='competitions'),
    path('register/', views.CreateUserView.as_view(), name='register'),
]