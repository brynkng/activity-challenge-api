from .fitbit_api_gateway import FitbitApiGateway
from functools import reduce


class PointCalculator:
    def __init__(self, gateway: FitbitApiGateway):
        self.gateway = gateway

    def calculate(self, competition, init_data, profile):
        point_system = competition.point_system

        start = competition.start.strftime('%Y-%m-%d')
        end = competition.end.strftime('%Y-%m-%d')

        init_data['fairly_active_data'] = self.__retrieve_activity_data(
            profile,
            start,
            end,
            'minutesFairlyActive'
        )

        init_data['very_active_data'] = self.__retrieve_activity_data(
            profile,
            start,
            end,
            'minutesVeryActive'
        )

        init_data['heart_rate_data'] = self.gateway.get_heart_data(start, end, profile)

        active_minutes = (self.__get_active_minutes(init_data['fairly_active_data']) +
                          self.__get_active_minutes(init_data['very_active_data']))

        cardio_zone_minutes = self.__get_hr_minutes('Cardio', init_data)
        peak_zone_minutes = self.__get_hr_minutes('Peak', init_data)

        init_data['points'] = ((point_system.active_minute_points * active_minutes) + 
            (point_system.cardio_zone_points * cardio_zone_minutes) + 
            (point_system.peak_zone_points * peak_zone_minutes))

        init_data['active_minutes'] = active_minutes
        init_data['cardio_zone_minutes'] = cardio_zone_minutes
        init_data['peak_zone_minutes'] = peak_zone_minutes
        init_data['active_minute_factor'] = point_system.active_minute_points
        init_data['cardio_zone_factor'] = point_system.cardio_zone_points
        init_data['peak_zone_factor'] = point_system.peak_zone_points

        return init_data

    def __retrieve_activity_data(self, profile, start, end, key):
        return self.gateway.get_activities_data(profile, start, end, key)

    def __get_active_minutes(self, data):
        return reduce((lambda acc, r: int(r['value']) + acc), data, 0)

    def __get_hr_minutes(self, key, init_data):
        return reduce(
            (lambda acc, r: int([i.get('minutes', 0) for i in r['value']
                                 ['heartRateZones'] if i['name'] == key][0]) + acc),
            init_data['heart_rate_data'], 0)
