import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.access_service import find_badge, find_role, is_access_allowed
from app.database import get_db
from app.schemas import BadgeResponse, RoleResponse


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
    authorized_roles: List[int] = Query(
        ...,
        description="IDs numériques des rôles autorisés",
    ),
    db: Session = Depends(get_db),
):
    allowed = is_access_allowed(db, badge_id, authorized_roles)

    logger.info(
        "Access decision recorded",
        extra={
            "event": "access_decision",
            "details": {
                "badge_id": badge_id,
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
    badge = find_badge(db, badge_id)

    if badge is None:
        raise HTTPException(status_code=404, detail="Badge introuvable")

    return BadgeResponse(
        id=badge.id,
        activation_date=badge.activation_date,
        ending_date=badge.ending_date,
        role_id=badge.role_id,
    )


@router.get("/role/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int = Path(
        ...,
        ge=100000000000,
        le=999999999999,
        description="ID numérique du rôle sur 12 chiffres",
    ),
    db: Session = Depends(get_db),
):
    role = find_role(db, role_id)

    if role is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")

    return RoleResponse(
        id=role.id,
        name=role.name,
    )