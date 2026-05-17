import uuid
from datetime import datetime
from urllib.parse import urlparse, urlunparse

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_url(v: str | None) -> str | None:
    if v is None:
        return v

    v = v.strip()

    parsed = urlparse(v)

    if parsed.scheme != "https":
        raise ValueError("URL must use https")

    if not parsed.netloc:
        raise ValueError("Invalid URL: Missing domain")

    path = parsed.path
    if path in ["/", ""]:
        path = ""

    normalized_url = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized_url


class MonitorCreate(BaseModel):
    name: str = Field(min_length=8, max_length=255)
    url: str
    check_interval: int = Field(default=30, ge=10, le=3600)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str):
        return normalize_url(v)


class MonitorUpdate(BaseModel):
    name: str | None
    url: str | None
    is_active: bool | None
    check_interval: int | None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str):
        return normalize_url(v)


class MonitorRead(BaseModel):
    id: uuid.UUID
    name: str
    url: str
    is_active: bool
    check_interval: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatsResponse(BaseModel):
    total_monitors: int
    active_monitors: int
    uptime_percentage: float
    average_response_time: float
