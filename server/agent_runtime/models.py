"""Agent runtime data models."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

SessionStatus = Literal["idle", "running", "completed", "error", "interrupted"]


class SessionMeta(BaseModel):
    """Session metadata stored in database."""

<<<<<<< HEAD
    id: str  # Công khai bên ngoài, điền giá trị sdk_session_id
=======
    id: str  # 对外暴露，填充 sdk_session_id 值
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    project_name: str
    title: str = ""
    status: SessionStatus = "idle"
    created_at: datetime
    updated_at: datetime


class AssistantSnapshotV2(BaseModel):
    """Unified assistant snapshot for history and reconnect."""

    session_id: str
    status: SessionStatus
    turns: list[dict[str, Any]]
    draft_turn: dict[str, Any] | None = None
    pending_questions: list[dict[str, Any]] = Field(default_factory=list)
