class ApiError(BaseException):
    def __init__(self, message):
        super().__init__(message)


class ApiAuthError(ApiError):
    def __init__(self, message):
        super().__init__(message)


