from dataclasses import dataclass, field
from typing import Any, Optional
from typing import Callable
from enum import Enum


@dataclass
class StoreResp:
    llm_response: Optional[Any] | None = None
    tool_name: Optional[str] | None = None
    arguments: Optional[list[dict[str, Any]]] | None = None
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


@dataclass
class MethodMatch:
    method_name: str
    match_percent: float   # raw similarity % (unweighted), 0-100
    user_message: str
    weight: int
    weighted_score: float  # match_percent * weight, used for ranking


@dataclass 
class ToolParameters:
    name: str = ""
    description: str = ""
    validationCallback: Callable[[Any], str | None] | None = None 

@dataclass
class ToolInfo:
    name: str = ""
    description: str = ""
    parameters: list[ToolParameters]  =  field(default_factory=list)

@dataclass
class UserChatReq:
    user_message: str
    llm_response: Optional[str] = None

class LlmProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

