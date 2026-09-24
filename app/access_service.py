from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import Badge, Role, ZoneAccess


def find_badge(db: Session, badge_id: int) -> Optional[Badge]:
    """Retourne un badge avec son rôle et son ou ses utilisateurs."""
    statement = (
        select(Badge)
        .options(joinedload(Badge.role), selectinload(Badge.users))
        .where(Badge.id == badge_id)
    )
    return db.execute(statement).scalar_one_or_none()


def is_access_allowed(db: Session, badge_id: int, authorized_roles: List[str]) -> bool:
    """Vérifie l'existence, la période de validité et le rôle du badge."""
    badge = find_badge(db, badge_id)

    if badge is None:
        return False

    today = date.today()
    if not badge.activation_date <= today <= badge.ending_date:
        return False

    # La liste contient les IDs des rôles qui sont autorisés pour la zone.
    return badge.role_id in authorized_roles


def find_role(db: Session, role_id: str) -> Optional[Role]:
    """Retourne un rôle et les zones auxquelles il donne accès."""
    statement = (
        select(Role)
        .options(selectinload(Role.zone_accesses).joinedload(ZoneAccess.zone))
        .where(Role.id == role_id)
    )
    return db.execute(statement).scalar_one_or_none()
