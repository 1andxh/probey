from pydantic import BaseModel


class QuickCheckResponse(BaseModel):
    url: str
    status_code: int | None = None
    latency_ms: float | None = None
    is_up: bool
    error: str | None = None
