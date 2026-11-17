
import uuid

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.base import utc_now


class Incident(db.Model):
    __tablename__ = "incidents"

    __table_args__ = (
        CheckConstraint(
            "severity IN ('low', 'medium', 'high', 'critical')",
            name="ck_incidents_severity",
        ),
        CheckConstraint(
            "status IN ('open', 'acknowledged', "
            "'investigating', 'resolved')",
            name="ck_incidents_status",
        ),
        Index(
            "ix_incidents_org_status_started",
            "organization_id",
            "status",
            "started_at",
        ),
    )

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    deployment_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("deployments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title = db.Column(
        String(255),
        nullable=False,
    )

    description = db.Column(
        Text,
        nullable=True,
    )

    severity = db.Column(
        String(30),
        nullable=False,
        default="medium",
    )

    status = db.Column(
        String(30),
        nullable=False,
        default="open",
    )

    started_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    resolved_at = db.Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    def __repr__(self):
        return f"<Incident {self.title} {self.severity}>"
