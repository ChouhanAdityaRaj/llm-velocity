from src.llm_velocity.models import models

def output_json(llm_response: str = "", tool_name: str = "", tool_arguments: dict[str, str] = None) -> models.StoreResp:
    """ Method to make look up output json response"""
    return models.StoreResp(
        llm_response=llm_response,
        tool_name=tool_name,
        arguments=tool_arguments,
    )