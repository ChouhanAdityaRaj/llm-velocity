from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class StoreResp:
    llm_response: Optional[Any] | None = None
    tool_name: Optional[str] | None = None
    arguments: Optional[dict[str, Any]] | None = None
    error: Optional[str] | None = None
    metadata: Optional[dict[str, Any]] | None = None

@dataclass
class ChatContext(StoreResp):
    user_message: str = ""
    created_at: Optional[int] | None = None
    id: int | None = None


@dataclass
class ToolOutput:
    name: str
    arguments: dict[str, str]
    