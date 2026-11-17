
import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


def utc_now():
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class CloudIntegration(db.Model):
    """Represents a cloud provider integration for an organization."""

    __tablename__ = "cloud_integrations"

    __table_args__ = (
        CheckConstraint(
            "provider IN ('aws', 'gcp', 'azure')",
            name="ck_cloud_integrations_provider",
        ),
        CheckConstraint(
            "status IN ('pending', 'connected', 'disconnected', 'error')",
            name="ck_cloud_integrations_status",
        ),
        UniqueConstraint(
            "organization_id",
            "provider",
            "integration_name",
            name="uq_org_cloud_integration",
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

    provider = db.Column(String(20), nullable=False)

    integration_name = db.Column(
        String(160),
        nullable=False,
    )

    status = db.Column(
        String(30),
        nullable=False,
        default="pending",
    )

    secret_ref = db.Column(
        String(512),
        nullable=False,
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
