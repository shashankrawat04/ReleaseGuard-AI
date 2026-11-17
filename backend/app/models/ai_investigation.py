
import uuid

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.extensions import db
from app.models.base import utc_now


class AIInvestigation(db.Model):
    __tablename__ = "ai_investigations"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed')",
            name="ck_ai_investigations_status",
        ),
        Index(
            "ix_ai_investigations_org_created",
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

    incident_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("incidents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    model = db.Column(
        String(160),
        nullable=True,
    )

    status = db.Column(
        String(30),
        nullable=False,
        default="pending",
    )

    hypothesis = db.Column(
        JSONB,
        nullable=True,
    )

    recommendations = db.Column(
        JSONB,
        nullable=False,
        default=list,
    )

    evidence = db.Column(
        JSONB,
        nullable=False,
        default=list,
    )

    token_usage = db.Column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    completed_at = db.Column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    def __repr__(self):
        return f"<AIInvestigation {self.status}>"
