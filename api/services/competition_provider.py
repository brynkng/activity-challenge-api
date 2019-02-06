from api.services.fitbit_provider import FitbitProvider
import os
import traceback
import pytz
from django.utils import timezone
from api.custom_errors import ApiAuthError, ApiError
from api.models import Profile, CompetitionInvitation, CompetitionScore, Competition
from datetime import datetime, time
from .point_calculator import PointCalculator

class CompetitionProvider(FitbitProvider):
    def simple_competitions(self, profile):
        return self.__build_simple_competitions_data(profile)


    def detailed_competition(profile, competition_id):
        competition = Competition.objects.filter(id=competition_id).last()

        return self.__build_detailed_competition(profile, competition)


    def __build_simple_competitions_data(self, profile):
        return {'competitions': [self.__build_simple_competition(profile, competition) for competition in
                                profile.competitions.all()]}


    def __update_competition_scores(self, competition):
        scores = []

        for profile in competition.profile_set.all():
            score = profile.competition_scores.filter(
                competition_id=competition.id).last()

            competition_end = datetime(competition.end.year, competition.end.month, competition.end.day, 23, 59, 59,
                                    tzinfo=pytz.UTC)

            score_out_of_date = score and ((competition.has_ended() and score.updated_at < competition_end) or (
                not competition.has_ended() and score.updated_at + timezone.timedelta(minutes=10) < timezone.now()))

            if not score:
                data = PointCalculator(self.gateway).calculate(competition, {}, profile)
                score = CompetitionScore.objects.create(
                    point_total=data.get('points'),
                    competition=competition,
                    profile=profile
                )
                score.save()

            elif score_out_of_date:
                data = PointCalculator(self.gateway).calculate(competition, {}, profile)
                score.point_total = data.get('points')
                score.save()

            scores.append(score)

        return scores


    def __build_simple_competition(self, profile, competition):
        scores = self.__update_competition_scores(competition)
        score = [score for score in scores if profile.id == score.profile.id][0]
        data = self.__base_competition_data(competition, scores)
        data['points'] = score.point_total

        return data


    def __get_winner(self, competition, scores=None):
        if competition.has_ended():
            if not scores:
                scores = _update_competition_scores(competition)

            scores.sort(key=lambda s: s.point_total)
            winner = scores[-1]

            return {'name': winner.profile.display_name, 'points': winner.point_total}
        else:
            return None


    def __base_competition_data(self, competition, scores=None):
        return {
            'id': competition.id,
            'name': competition.name,
            'start': competition.start,
            'end': competition.end.strftime('%Y-%m-%d'),
            'current': not competition.has_ended(),
            'winner': self.__get_winner(competition, scores)
        }

    def __competition_friend_list(profile, competition):
        friends_response = get_friends(profile)
        fitbit_ids = [f['user']['encodedId'] for f in friends_response]

        # TODO possibly clean this up just working with profile querysets? preload competitions and invitations?
        id_tuples = Profile.objects.filter(
            fitbit_user_id__in=fitbit_ids).values_list('id', 'fitbit_user_id')
        profile_to_fitbit = {ids[0]: ids[1] for ids in id_tuples}
        fitbit_to_profile = {ids[1]: ids[0] for ids in id_tuples}
        in_competition = Profile.competitions.through.objects.filter(
            competition_id=competition.id,
            profile_id__in=profile_to_fitbit.keys()
        ).values_list('profile_id', flat=True)

        def _build_friend_list(f):
            info = f['user']
            fitbit_id = info['encodedId']
            profile_id = fitbit_to_profile.get(fitbit_id, None)
            invited = CompetitionInvitation.objects.filter(
                profile=profile_id, competition=competition.id).exists()

            return {
                'display_name': info['displayName'],
                'avatar': info['avatar'],
                'in_app': fitbit_id in fitbit_to_profile,
                'in_competition': profile_id in in_competition,
                'invited': invited,
                'profile_id': profile_id,
                'fitbit_id': fitbit_id
            }

        return list(map(_build_friend_list, friends_response))


    def __build_detailed_competition(self, profile, competition):
        friend_list = self.__competition_friend_list(profile, competition)
        profile_ids = [f['profile_id'] for f in friend_list]
        profiles = Profile.objects.filter(id__in=profile_ids)

        def _get_profile(id): return [p for p in profiles if p.id == id][0]

        competition_members = [
            PointCalculator(self.gateway).calculate(competition, f, _get_profile(f['profile_id']))
            for f in friend_list if f['in_competition']
        ]

        invitable_friends = [
            f for f in friend_list if f['in_app'] and not f['in_competition']]

        data = self.__base_competition_data(competition)
        data['point_details'] = PointCalculator(self.gateway).calculate(competition, {}, profile)
        data['competition_members'] = competition_members
        data['invitable_friends'] = invitable_friends

        return data
