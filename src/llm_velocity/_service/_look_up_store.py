from src.llm_velocity._engine import _database_exec, _ollama_exec, _semantic_search, _text_search
from src.llm_velocity._engine import _tool_definition_store
from src.llm_velocity._utils import _utils
from src.llm_velocity._models import _models

class _LookUpStore:
    def __init__(self, database_exec_obj: _database_exec._DatabaseExec, semantic_search_obj: _semantic_search._SemanticSearch, ollama_exec_obj: _ollama_exec._OllamaExec, tool_definition_store_obj: _tool_definition_store._ToolDefinitionStore):
        self.__database_exec_obj: _database_exec._DatabaseExec = database_exec_obj
        self.__semantic_search_obj: _semantic_search._SemanticSearch = semantic_search_obj
        self.__ollama_exec_obj: _ollama_exec._OllamaExec = ollama_exec_obj
        self.__tool_definition_store_obj: _tool_definition_store._ToolDefinitionStore = tool_definition_store_obj

    def search_in_store(self, user_message: str) -> _models.StoreResp | None:

        db_user_message_list =  self.__database_exec_obj.get_all_chat_user_message() #! optimize this latter
        chat_id: int = None
        # 1. text based search
        chat_id = _text_search._TextSearch.search_text(db_user_message_list, user_message)
        if chat_id == None:
            # 2. semantic_search (if user message not found in text based)
            chat_id = self.__semantic_search_obj.search_index(user_message)

        if chat_id == None: 
            return None
            
        # 5. Get chat context
        chat_detils = self.__database_exec_obj.get_chat_context(chat_id)
    
        if chat_detils.tool_name == "":
            # 4. if no tool calling retuen normal response
            return _utils.output_json(chat_detils.llm_response)
        else:
            # 5. if tool call then send tool name with arguments 
            tool_paramaters = self.__tool_definition_store_obj.get_tool_definition(chat_detils.tool_name)

            llm_resp, arguments = self.__ollama_exec_obj.extract_argument(user_message, tool_paramaters)

            return _utils.output_json(llm_resp, chat_detils.tool_name, arguments)
        
        
    def add_to_store(self, chat_context: _models.ChatContext) -> None:
        self.__semantic_search_obj.add_to_index([chat_context.user_message])
        self.__database_exec_obj.store_chat_context(chat_context)
        return



             