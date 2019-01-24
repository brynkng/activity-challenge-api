from django.urls import path

from . import views

urlpatterns = [
    path('competitions/<int:competition_id>', views.competition_details),
    path('competitions/', views.simple_competitions_list),
    path('competitions/', views.CompetitionCreate.as_view()),
    path('competition_invitations/', views.CompetitionInvitationCreate.as_view(), name='competition_invitations'),
    path('competition_invitations/<int:pk>', views.CompetitionInvitationUpdate.as_view()),
    path('register/', views.CreateUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('store_fitbit_auth/', views.fitbit_store_auth),
]