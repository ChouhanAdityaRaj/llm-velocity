import json
from pathlib import Path

class _ToolDefinitionStore:
    def __init__(self, json_file_path: str):
        self.__json_file_path: str = Path(json_file_path)
        self.__tool_definition_obj: dict[str, list[str]]

    def load_tools(self) -> None:
        with open(self.__json_file_path, "r", encoding="utf-8") as f:
            self.__tool_definition_obj = json.load(f)

    def get_tool_definition(self, tool_name: str) -> list[str]:
        return self.__tool_definition_obj[tool_name]
