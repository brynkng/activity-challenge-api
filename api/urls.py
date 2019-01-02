from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('competitions/<int:competition_id>', views.competition, name='competition'),
    path('competitions/', views.CompetitionListCreate.as_view(), name='competitions'),
]