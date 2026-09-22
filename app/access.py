from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.access_service import find_badge, find_role, is_access_allowed
from app.database import get_db
from app.schemas import BadgeResponse, RoleResponse, UserResponse, ZoneResponse

router = APIRouter(tags=["Access control"])


@router.get("/access/check", response_model=bool)
def check_access(
    badge_id: str = Query(..., description="ID du badge lu par le hardware"),
    authorized_roles: List[str] = Query(
        ..., description="IDs des rôles autorisés dans la zone demandée"
    ),
    db: Session = Depends(get_db),
):
    """Retourne true si le badge est valide et son rôle est autorisé."""
    return is_access_allowed(db, badge_id, authorized_roles)


@router.get("/badge/{badge_id}", response_model=BadgeResponse)
def get_badge(badge_id: str, db: Session = Depends(get_db)):
    """Retourne les informations complètes d'un badge."""
    badge = find_badge(db, badge_id)
    if badge is None:
        raise HTTPException(status_code=404, detail="Badge introuvable")

    return BadgeResponse(
        id=badge.id,
        activation_date=badge.activation_date,
        ending_date=badge.ending_date,
        role_id=badge.role_id,
        role_name=badge.role.name,
        users=[
            UserResponse(
                id=user.id,
                name=user.name,
                surname=user.surname,
                birthdate=user.birthdate,
                sex=user.sex,
                email=user.email,
                badge_id=user.badge_id,
            )
            for user in badge.users
        ],
    )


@router.get("/role/{role_id}", response_model=RoleResponse)
def get_role(role_id: str, db: Session = Depends(get_db)):
    """Retourne un rôle et les zones accessibles avec ce rôle."""
    role = find_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")

    return RoleResponse(
        id=role.id,
        name=role.name,
        zones=[
            ZoneResponse(id=access.zone.id, name=access.zone.name)
            for access in role.zone_accesses
        ],
    )
