from src.llm_velocity.service.look_up_store import LookUpStore
from src.llm_velocity.engine import database_exec, ollama_exec, semantic_search, tool_definition_store, storage
from sentence_transformers import SentenceTransformer
from src.llm_velocity.models.models import ChatContext
from src.llm_velocity.constants import constants
from src.llm_velocity.models import models
from src.llm_velocity.utils import utils

class LLMLookUpStore:
    def __init__(self, ollama_model: str, ollama_url: str, tools_json_file_path: str):
        self__storage_obj : storage.Storage
        self.__ollama_model: str = ollama_model
        self.__ollama_url: str = ollama_url
        self.__tools_json_file_path: str = tools_json_file_path
        self.__database_exec_obj: database_exec.DatabaseExec 
        self.__semantic_search_obj: semantic_search.SemanticSearch
        self.__ollama_exec_obj: ollama_exec.OllamaExec
        self.__tool_definition_store_obj: tool_definition_store.ToolDefinitionStore
        self.__cache_manager_obj: LookUpStore

    def init_setup(self) -> None:
        """Initial setup of class"""
        self__storage_obj = storage.Storage(constants.PROJECT_NAME, constants.DATABASE_NAME, constants.INDEX_NAME)
        self.__database_exec_obj = database_exec.DatabaseExec(self__storage_obj.database_path)
        self.__ollama_exec_obj = ollama_exec.OllamaExec(self.__ollama_url, self.__ollama_model)
        self.__semantic_search_obj = semantic_search.SemanticSearch(SentenceTransformer(constants.SENTENCE_TRANSORMER_MODEL), self__storage_obj.index_path)
        self.__tool_definition_store_obj = tool_definition_store.ToolDefinitionStore(self.__tools_json_file_path)
        self.__cache_manager_obj = LookUpStore(self.__database_exec_obj, self.__semantic_search_obj, self.__ollama_exec_obj, self.__tool_definition_store_obj)

        self.__database_exec_obj.init_tables()
        self.__semantic_search_obj.load_index_from_file()
        self.__tool_definition_store_obj.load_tools()

    def call_store(self, chat_message: str) -> models.StoreResp | None :

        logical_context = utils.extract_logical_context(chat_message)

        look_up_store_res =  self.__cache_manager_obj.search_in_store(chat_message, logical_context)
        if look_up_store_res != None:
            # print("from store")
            return look_up_store_res

        ollama_call_res = self.__ollama_exec_obj.call(chat_message);

        if ollama_call_res.tool_name != None or ollama_call_res.llm_response != None :
            self.__cache_manager_obj.add_to_store(ChatContext(
                llm_response=ollama_call_res.llm_response,
                tool_name=ollama_call_res.tool_name,
                user_message=logical_context
            ))
            # print("from ollama")
            return ollama_call_res

        return  models.StoreResp(error="not_found")