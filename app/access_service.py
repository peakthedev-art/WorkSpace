from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import Badge, Role


def find_badge(db: Session, badge_id: int) -> Optional[Badge]:
    statement = (
        select(Badge)
        .options(joinedload(Badge.role), selectinload(Badge.users))
        .where(Badge.id == badge_id)
    )
    return db.execute(statement).scalar_one_or_none()


def is_access_allowed(
    db: Session,
    badge_id: int,
    authorized_roles: List[int],
) -> bool:
    badge = find_badge(db, badge_id)

    if badge is None:
        return False

    today = date.today()
    if not badge.activation_date <= today <= badge.ending_date:
        return False

    return badge.role_id in authorized_roles


def find_role(db: Session, role_id: int) -> Optional[Role]:
    statement = select(Role).where(Role.id == role_id)
    return db.execute(statement).scalar_one_or_none()