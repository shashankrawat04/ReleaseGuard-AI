
import uuid

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.base import utc_now


class Service(db.Model):
    __tablename__ = "services"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "environment",
            "resource_identifier",
            name="uq_service_org_environment_resource",
        ),
        CheckConstraint(
            "status IN ('active', 'inactive', 'unknown')",
            name="ck_services_status",
        ),
        CheckConstraint(
            "environment IN ('development', 'staging', 'production')",
            name="ck_services_environment",
        ),
        Index(
            "ix_services_org_created",
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

    integration_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("cloud_integrations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name = db.Column(
        String(160),
        nullable=False,
    )

    environment = db.Column(
        String(30),
        nullable=False,
    )

    resource_identifier = db.Column(
        String(512),
        nullable=False,
    )

    status = db.Column(
        String(30),
        nullable=False,
        default="active",
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
        return f"<Service {self.name}>"
