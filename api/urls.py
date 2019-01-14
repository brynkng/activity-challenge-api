from django.urls import path

from . import views

urlpatterns = [
    path('competition_invitations/', views.CompetitionInvitationCreate.as_view(), name='competition_invitations'),
    path('competition_invitations/<int:pk>', views.CompetitionInvitationUpdate.as_view()),
    path('register/', views.CreateUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('fitbit_data/', views.fitbit_data),
    path('store_fitbit_auth/', views.fitbit_store_auth),
]