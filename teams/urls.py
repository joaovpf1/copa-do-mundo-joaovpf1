from django.urls import path
from teams.views import TeamView, TeamViewDetail

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamViewDetail.as_view()),
]
