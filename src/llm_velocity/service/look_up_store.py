from src.llm_velocity.engine import database_exec, semantic_search, llm_exec, tool_definition_store, text_search
from src.llm_velocity.utils import utils
from src.llm_velocity.models import models

class LookUpStore:
    def __init__(self, database_exec_obj: database_exec.DatabaseExec, semantic_search_obj: semantic_search.SemanticSearch, llm_exec_obj: llm_exec.LLMExec, tool_definition_store_obj: tool_definition_store.ToolDefinitionStore):
        self.__database_exec_obj: database_exec.DatabaseExec = database_exec_obj
        self.__semantic_search_obj: semantic_search.SemanticSearch = semantic_search_obj

    def search_in_store(self, user_message: str) -> models.StoreResp | None:

        db_user_message_list =  self.__database_exec_obj.get_all_chat_user_message() #! optimize this latter
        chat_id: int = None
        # 1. text based search
        chat_id = text_search.TextSearch.search_text(db_user_message_list, user_message)
        if chat_id == None:
            # 2. semantic_search (if user message not found in text based)
            chat_id = self.__semantic_search_obj.search_index(user_message)

        if chat_id == None: 
            return None
            
        # 5. Get chat context
        chat_details = self.__database_exec_obj.get_chat_context(chat_id)
    
        return utils.output_json(chat_details.llm_response)
        
    def add_to_store(self, chat_context: models.ChatContext) -> None:
        self.__semantic_search_obj.add_to_index([chat_context.user_message])
        self.__database_exec_obj.store_chat_context(chat_context)
        return



             