import json
from pathlib import Path
from src.llm_velocity.models import models

class ToolDefinitionStore:
    def __init__(self, tool_definition: dict[str, models.ToolInfo]):
        self.__tool_info: dict[str, models.ToolInfo] = tool_definition

    def get_all_tool_definition(self) ->  dict[str, models.ToolInfo]:
        return self.__tool_info
    
    def get_tool_definition(self, tool_name: str) ->  models.ToolInfo:
        return self.__tool_info[tool_name]
