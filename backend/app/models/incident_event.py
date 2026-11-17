
import uuid

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.extensions import db
from app.models.base import utc_now


class IncidentEvent(db.Model):
    __tablename__ = "incident_events"

    __table_args__ = (
        Index(
            "ix_incident_events_org_created",
            "organization_id",
            "created_at",
        ),
        Index(
            "ix_incident_events_incident_created",
            "incident_id",
            "created_at",
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

    incident_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("incidents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type = db.Column(
        String(100),
        nullable=False,
    )

    event_data = db.Column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    def __repr__(self):
        return f"<IncidentEvent {self.event_type}>"
