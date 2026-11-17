
import uuid

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Text,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.base import utc_now


class Deployment(db.Model):
    __tablename__ = "deployments"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'deploying', 'succeeded', "
            "'failed', 'rolled_back')",
            name="ck_deployments_status",
        ),
        Index(
            "ix_deployments_org_service_deployed",
            "organization_id",
            "service_id",
            "deployed_at",
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

    commit_sha = db.Column(
        String(100),
        nullable=True,
    )

    version = db.Column(
        String(100),
        nullable=True,
    )

    status = db.Column(
        String(30),
        nullable=False,
        default="pending",
    )

    source = db.Column(
        String(100),
        nullable=True,
    )

    deployed_at = db.Column(
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

    description = db.Column(
        Text,
        nullable=True,
    )

    def __repr__(self):
        return f"<Deployment {self.version} {self.status}>"
