from src.llm_velocity.service.look_up_store import LookUpStore
from src.llm_velocity.service.tool_extractor import ToolExtractor
from src.llm_velocity.engine import database_exec, llm_exec, semantic_search, tool_definition_store, storage
from sentence_transformers import SentenceTransformer
from src.llm_velocity.models.models import ChatContext
from src.llm_velocity.constants import constants
from src.llm_velocity.models import models
from src.llm_velocity.utils import utils

class LLMLookUpStore:
    def __init__(self,llm_provider: str, llm_model: str, endpoint_url: str, api_key: str, tools_definition: dict[str, models.ToolInfo], llm_temperature: float = 0.7):
        self.__storage_obj : storage.Storage
        self.__llm_provider: str = llm_provider
        self.__llm_model: str = llm_model
        self.__endpoint_url: str = endpoint_url
        self.__api_key: str = api_key
        self.__llm_temperature: float = llm_temperature
        self.__tools_definition: dict[str, models.ToolInfo] = tools_definition
        self.__database_exec_obj: database_exec.DatabaseExec 
        self.__semantic_search_obj: semantic_search.SemanticSearch
        self.__llm_exec_obj: llm_exec.LLMExec
        self.__tool_definition_store_obj: tool_definition_store.ToolDefinitionStore
        self.__cache_manager_obj: LookUpStore
        self.__tool_extractor_obj: ToolExtractor

    def init_setup(self) -> None:
        """Initial setup of class"""
        self.__storage_obj = storage.Storage(constants.PROJECT_NAME, constants.DATABASE_NAME, constants.INDEX_NAME)
        self.__database_exec_obj = database_exec.DatabaseExec(self.__storage_obj.database_path)
        self.__llm_exec_obj = llm_exec.LLMExec(self.__llm_provider, self.__endpoint_url, self.__llm_model, self.__api_key, self.__llm_temperature)
        self.__semantic_search_obj = semantic_search.SemanticSearch(SentenceTransformer(constants.SENTENCE_TRANSFORMER_MODEL), self.__storage_obj.index_path)
        self.__tool_definition_store_obj = tool_definition_store.ToolDefinitionStore(self.__tools_definition)
        self.__cache_manager_obj = LookUpStore(self.__database_exec_obj, self.__semantic_search_obj, self.__llm_exec_obj, self.__tool_definition_store_obj)
        self.__tool_extractor_obj = ToolExtractor(self.__semantic_search_obj, self.__llm_exec_obj, self.__tool_definition_store_obj)

        self.__database_exec_obj.init_tables()
        self.__semantic_search_obj.load_index_from_file()

    def call(self, chat_context: list[models.UserChatReq], is_tool_calling: bool = False) -> models.StoreResp | None :

        # tool calling defiled 
        if not is_tool_calling:

            # Extract first user message
            none_tool_calling_user_message: str = chat_context[0].user_message

            # search in store if found any thing return that response
            look_up_store_res =  self.__cache_manager_obj.search_in_store(none_tool_calling_user_message)
            if look_up_store_res != None:
                print("from store")
                return look_up_store_res
            
            # if store data is none call ollama
            ollama_call_res = self.__llm_exec_obj.call(none_tool_calling_user_message)

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
            resp = self.__tool_extractor_obj.extract_tool_info(chat_context=chat_context)

            return resp