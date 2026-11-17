
import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


def utc_now():
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class Organization(db.Model):
    """Represents an organization using ReleaseGuard-AI."""

    __tablename__ = "organizations"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = db.Column(String(160), nullable=False)

    slug = db.Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class User(db.Model):
    """Represents an individual user."""

    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email = db.Column(
        String(320),
        nullable=False,
        unique=True,
        index=True,
    )

    name = db.Column(String(160), nullable=False)

    cognito_sub = db.Column(
        String(255),
        unique=True,
        nullable=True,
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class OrganizationMember(db.Model):
    """Connects users to organizations and defines their roles."""

    __tablename__ = "organization_members"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_org_member",
        ),
        CheckConstraint(
            "role IN ('owner', 'admin', 'developer', 'viewer')",
            name="ck_org_member_role",
        ),
    )

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    role = db.Column(
        String(40),
        nullable=False,
        default="developer",
    )

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
