from datetime import date

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    birthdate: date
    sex: str
    email: str
    badge_id: str


class BadgeResponse(BaseModel):
    id: str
    activation_date: date
    ending_date: date
    role_id: str


class ZoneResponse(BaseModel):
    id: str
    name: str


class RoleResponse(BaseModel):
    id: str
    name: str