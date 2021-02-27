"""
File contains the definitions of all exception classes used throughout the Enrollment service.
"""

class ServiceUnavailableException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message


class MissingRequestBodyException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message


class OtpKeyLengthException(Exception):
    pass


class MobileNumberLengthException(Exception):
    pass


class MobileNumberInvalidException(Exception):
    pass


class AppIdLoginUserException(Exception):
    pass


class AppIdUserProfileException(Exception):
    pass


class AppIdCreateUserException(Exception):
    pass


class AppIdIamAccessTokenException(Exception):
    pass


class AppIdIntrospectException(Exception):
    pass


class AppIdRefreshTokenException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message


class AppIdRevokeTokenException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message


class MissingHeadersException(Exception):
    pass


class UsernameInvalidException(Exception):
    pass


class FullNameTooShortException(Exception):
    pass


class GatewayTimeoutException(Exception):
    pass


class InvalidURLException(Exception):
    pass


class AppIdTokensExpiredException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message


class EdxCourseNotFound(Exception):
    pass

class AuthenticationError(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message

class AuthorizationError(Exception):
    
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message

class BadRequestException(Exception):
    def __init__(self, message_code: str=None, message: str=None):
        self.message_code = message_code
        self.message = message
