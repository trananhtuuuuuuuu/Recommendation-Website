from .base import BaseAPIException

class NotFoundException(BaseAPIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")

class UnauthorizedException(BaseAPIException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")

class DuplicateResourceException(BaseAPIException):
  def __init__(self, message: str = "Duplicate resources"):
    super().__init__(message, error_code="Invalid resoures")