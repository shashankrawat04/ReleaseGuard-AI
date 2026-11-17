
import uuid

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.extensions import db
from app.models.base import utc_now


class IntegrationEvent(db.Model):
    __tablename__ = "integration_events"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "provider",
            "idempotency_key",
            name="uq_integration_event_idempotency",
        ),
        CheckConstraint(
            "provider IN ('aws', 'gcp', 'azure', 'github', 'gitlab', 'other')",
            name="ck_integration_events_provider",
        ),
        CheckConstraint(
            "processing_status IN "
            "('pending', 'processing', 'processed', 'failed')",
            name="ck_integration_events_status",
        ),
        CheckConstraint(
            "retry_count >= 0",
            name="ck_integration_events_retry_count",
        ),
        Index(
            "ix_integration_events_org_created",
            "organization_id",
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

    provider = db.Column(
        String(30),
        nullable=False,
    )

    event_type = db.Column(
        String(160),
        nullable=False,
    )

    payload = db.Column(
        JSONB,
        nullable=True,
    )

    payload_ref = db.Column(
        String(512),
        nullable=True,
    )

    processing_status = db.Column(
        String(30),
        nullable=False,
        default="pending",
    )

    retry_count = db.Column(
        Integer,
        nullable=False,
        default=0,
    )

    idempotency_key = db.Column(
        String(255),
        nullable=False,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    processed_at = db.Column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self):
        return f"<IntegrationEvent {self.provider} {self.processing_status}>"
