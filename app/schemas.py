from datetime import date

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    birthdate: date
    sex: str
    email: str
    badge_id: int


class BadgeResponse(BaseModel):
    id: int
    activation_date: date
    ending_date: date
    role_id: int


class ZoneResponse(BaseModel):
    id: str
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str