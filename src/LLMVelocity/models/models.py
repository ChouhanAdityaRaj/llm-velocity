from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ChatContext:
    user_message: str
    tool_name: str
    llm_response: Any
    created_at: Optional[int] = None
    id: int | None = None


@dataclass
class ToolOutput:
    name: str
    arguments: dict[str, str]
    
@dataclass
class LookUpOutput:
    message: Optional[str] = None
    tool: Optional[ToolOutput] = None
