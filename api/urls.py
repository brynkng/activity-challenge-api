from django.urls import path

from . import views

urlpatterns = [
    path('competitions/', views.CompetitionListCreate.as_view(), name='competitions'),
    path('register/', views.CreateUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('fitbit_data/', views.fitbit_data),
    path('store_fitbit_auth/', views.fitbit_store_auth),
    path('competition_friend_list/<int:competition_id>/', views.competition_friend_list),
]