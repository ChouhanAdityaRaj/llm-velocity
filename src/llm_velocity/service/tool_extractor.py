from src.llm_velocity.engine import llm_exec, semantic_search, tool_definition_store
from src.llm_velocity.models import models
from src.llm_velocity.utils import utils


class ToolExtractor:
    def __init__(self, semantic_search_obj: semantic_search.SemanticSearch, llm_exec_obj: llm_exec.LLMExec, tool_definition_store_obj: tool_definition_store.ToolDefinitionStore):
        self.__semantic_search_obj: semantic_search.SemanticSearch = semantic_search_obj
        self.__llm_exec_obj: llm_exec.LLMExec = llm_exec_obj
        self.__tool_definition_store_obj: tool_definition_store.ToolDefinitionStore = tool_definition_store_obj

    def extract_tool_info(self, chat_context: list[models.UserChatReq]) -> models.StoreResp | None:

        tool_description: dict[str, str] = {}
        filter_user_messages: list[str] = [user_message.user_message for user_message in chat_context]

        for tool_name, tool_details in self.__tool_definition_store_obj.get_all_tool_definition().items():
            tool_description[tool_name] = tool_details.description

        tool_matching_details = self.__semantic_search_obj.match_best_method(filter_user_messages, tool_description)

        tool_details = self.__tool_definition_store_obj.get_tool_definition(tool_matching_details.method_name)

        if len(tool_details.parameters) == 0:
            return utils.output_json(tool_name=tool_details.name)

        formatted_parameters: list[tuple[str, str]] = []

        for parameter in tool_details.parameters:
            formatted_parameters.append((parameter.name, parameter.description))

        arguments = self.__llm_exec_obj.extract_argument(chat_context, formatted_parameters)

        validation_err : list[str] = []

        for parameter in tool_details.parameters:
            validation_err_msg = parameter.validationCallback(arguments.get(parameter.name))
            if validation_err_msg == None:
                continue
            validation_err.append(validation_err_msg)

        return utils.output_json("\n".join(validation_err), tool_details.name, arguments)