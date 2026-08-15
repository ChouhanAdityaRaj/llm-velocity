from src.llm_velocity.models import models
from src.llm_velocity.constants import constants

def output_json(llm_response: str = "", tool_name: str = "", tool_arguments: dict[str, str] = None) -> models.StoreResp:
    """ Method to make look up output json response"""
    return models.StoreResp(
        llm_response=llm_response,
        tool_name=tool_name,
        arguments=tool_arguments,
    )

def extract_logical_context(full_context: str):
    return full_context.split(constants.USER_MESSAGE_PROPERTY, 1)[0].strip()