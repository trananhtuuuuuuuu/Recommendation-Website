# app/models/enums.py
import enum

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"

class ApplicantStatus(str, enum.Enum):
    OpenToWork = "OpenToWork"
    Archived = "Archived"

class MethodEnum(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"