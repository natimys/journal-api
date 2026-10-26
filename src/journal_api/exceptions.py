class BaseException(Exception):
    pass

class UnauthorizedException(BaseException):
    pass

class ForbiddenException(BaseException):
    pass

class NotFoundException(BaseException):
    pass

class RateLimitException(BaseException):
    pass

class BadRequestException(BaseException):
    pass

class InternalServerException(BaseException):
    pass

class ServiceUnavailableException(BaseException):
    pass