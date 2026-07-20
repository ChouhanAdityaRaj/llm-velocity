from src.LLMVelocity.models import models

def output_json(message: str = "", tool_name: str = "", tool_arguments: dict[str, str] = None) -> str:
    """ Method to make look up output json response"""
    return models.LookUpOutput(
        message=message,
        tool=models.ToolOutput(
            name=tool_name,
            arguments=tool_arguments,
        )
    )