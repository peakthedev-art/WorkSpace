from datetime import date
from typing import List

from sqlalchemy import Date, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(Base):
    __tablename__ = "role"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    badges: Mapped[List["Badge"]] = relationship(back_populates="role")
    zone_accesses: Mapped[List["ZoneAccess"]] = relationship(back_populates="role")


class Badge(Base):
    __tablename__ = "badge"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    activation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=text("CURRENT_DATE"),
    )
    ending_date: Mapped[date] = mapped_column(Date, nullable=False)
    role_id: Mapped[str] = mapped_column(
        ForeignKey("role.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(back_populates="badges")
    users: Mapped[List["User"]] = relationship(back_populates="badge")


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    badge_id: Mapped[str] = mapped_column(
        ForeignKey("badge.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    badge: Mapped["Badge"] = relationship(back_populates="users")
    habitations: Mapped[List["Habitation"]] = relationship(back_populates="owner")


class Habitation(Base):
    __tablename__ = "habitation"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(back_populates="habitations")


class Zone(Base):
    __tablename__ = "zone"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    zone_accesses: Mapped[List["ZoneAccess"]] = relationship(back_populates="zone")


class ZoneAccess(Base):
    __tablename__ = "zone_access"

    role_id: Mapped[str] = mapped_column(
        ForeignKey("role.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )
    zone_id: Mapped[str] = mapped_column(
        ForeignKey("zone.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )

    role: Mapped["Role"] = relationship(back_populates="zone_accesses")
    zone: Mapped["Zone"] = relationship(back_populates="zone_accesses")