import logging
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.access_service import find_badge, find_role, is_access_allowed
from app.database import get_db
from app.schemas import BadgeResponse, RoleResponse, UserResponse, ZoneResponse

router = APIRouter(tags=["Access control"])
logger = logging.getLogger(__name__)


@router.get("/access/check", response_model=bool)
def check_access(
    badge_id: int = Query(
        ...,
        ge=100000000000,
        le=999999999999,
        description="ID numérique du badge RFID sur 12 chiffres",
    ),
    authorized_roles: List[str] = Query(
        ...,
        description="IDs des rôles autorisés dans la zone demandée",
    ),
    zone: Optional[str] = Query(
        None,
        description="Nom de la zone demandée",
    ),
    db: Session = Depends(get_db),
):
    """Retourne true si le badge est valide et son rôle est autorisé."""
    allowed = is_access_allowed(db, badge_id, authorized_roles)

    logger.info(
        "Access decision recorded",
        extra={
            "event": "access_decision",
            "details": {
                "badge_id": badge_id,
                "zone": zone or "unknown",
                "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
                "authorized": allowed,
            },
        },
    )

    return allowed


@router.get("/badge/{badge_id}", response_model=BadgeResponse)
def get_badge(
    badge_id: int = Path(
        ...,
        ge=100000000000,
        le=999999999999,
        description="ID numérique du badge RFID sur 12 chiffres",
    ),
    db: Session = Depends(get_db),
):
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