from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.probe.models import Probe
    from src.users.models import User


class Monitor(Base):
    # specific target to watch

    __tablename__ = "monitors"

    __table_args__ = (
        UniqueConstraint("url", name="uq_monitor_url"),
        CheckConstraint(
            "url LIKE 'http://%' OR url LIKE 'https://%'", name="check_url_protocol"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    check_interval: Mapped[int] = mapped_column(server_default="30")
    last_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # relationships
    probes: Mapped[list["Probe"]] = relationship(
        "Probe",
        back_populates="monitor",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    owner: Mapped["User"] = relationship("User", back_populates="monitors")
