from rest_framework.views import APIView, status, Request, Response
from teams.models import Team
from utils import data_processing
from django.forms import model_to_dict
from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


# Create your views here.
class TeamView(APIView):
    def post(self, request: Request) -> Response:
        team_data = request.data
        try:
            data_processing(team_data)
            team = Team.objects.create(**team_data)
            converted_team = model_to_dict(team)
            return Response(converted_team, status.HTTP_201_CREATED)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as err:
            return Response(
                {"error": err.args[0]},
                status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        converted_teams = [model_to_dict(team) for team in teams]
        return Response(converted_teams, status.HTTP_200_OK)


class TeamViewDetail(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        converted_team = model_to_dict(team)
        return Response(converted_team, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )

        for key, value in request.data.items():
            setattr(team, key, value)
        team.save()
        converted_team = model_to_dict(team)
        return Response(converted_team, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
