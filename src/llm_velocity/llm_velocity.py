from src.llm_velocity.service.look_up_store import LookUpStore
from src.llm_velocity.service.tool_extractor import ToolExtractor
from src.llm_velocity.engine import database_exec, ollama_exec, semantic_search, tool_definition_store, storage
from sentence_transformers import SentenceTransformer
from src.llm_velocity.models.models import ChatContext
from src.llm_velocity.constants import constants
from src.llm_velocity.models import models
from src.llm_velocity.utils import utils

class LLMLookUpStore:
    def __init__(self, ollama_model: str, ollama_url: str, tools_definition: dict[str, models.ToolInfo]):
        self.__storage_obj : storage.Storage
        self.__ollama_model: str = ollama_model
        self.__ollama_url: str = ollama_url
        self.__tools_definition: dict[str, models.ToolInfo] = tools_definition
        self.__database_exec_obj: database_exec.DatabaseExec 
        self.__semantic_search_obj: semantic_search.SemanticSearch
        self.__ollama_exec_obj: ollama_exec.OllamaExec
        self.__tool_definition_store_obj: tool_definition_store.ToolDefinitionStore
        self.__cache_manager_obj: LookUpStore
        self.__tool_extractor_obj: ToolExtractor

    def init_setup(self) -> None:
        """Initial setup of class"""
        self.__storage_obj = storage.Storage(constants.PROJECT_NAME, constants.DATABASE_NAME, constants.INDEX_NAME)
        self.__database_exec_obj = database_exec.DatabaseExec(self.__storage_obj.database_path)
        self.__ollama_exec_obj = ollama_exec.OllamaExec(self.__ollama_url, self.__ollama_model)
        self.__semantic_search_obj = semantic_search.SemanticSearch(SentenceTransformer(constants.SENTENCE_TRANSFORMER_MODEL), self.__storage_obj.index_path)
        self.__tool_definition_store_obj = tool_definition_store.ToolDefinitionStore(self.__tools_definition)
        self.__cache_manager_obj = LookUpStore(self.__database_exec_obj, self.__semantic_search_obj, self.__ollama_exec_obj, self.__tool_definition_store_obj)
        self.__tool_extractor_obj = ToolExtractor(self.__semantic_search_obj, self.__ollama_exec_obj, self.__tool_definition_store_obj)

        self.__database_exec_obj.init_tables()
        self.__semantic_search_obj.load_index_from_file()

    def call_store(self, chat_messages: list[models.UserChatReq], is_tool_calling: bool = False) -> models.StoreResp | None :

        # tool calling defiled 
        if not is_tool_calling:

            # Extract first user message
            none_tool_calling_user_message: str = chat_messages[0].user_message

            # search in store if found any thing return that response
            look_up_store_res =  self.__cache_manager_obj.search_in_store(none_tool_calling_user_message)
            if look_up_store_res != None:
                print("from store")
                return look_up_store_res
            
            # if store data is none call ollama
            ollama_call_res = self.__ollama_exec_obj.call(none_tool_calling_user_message)

            # if ollama response is none return error
            if ollama_call_res == None :
                return  models.StoreResp(error="not_found")
            
            self.__cache_manager_obj.add_to_store(ChatContext(
                llm_response=ollama_call_res,
                user_message=none_tool_calling_user_message,
            ))
            print("from ollama")
            return ollama_call_res

        else:
            resp = self.__tool_extractor_obj.extract_tool_info(chat_messages)

            return resp