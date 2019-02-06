from api.services.fitbit_api_gateway import FitbitApiGateway


class FitbitProvider:
    def __init__(self, profile):
        self.gateway = FitbitApiGateway(profile)
