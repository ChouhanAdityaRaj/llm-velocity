from src.llm_velocity._engine import _database_exec, _ollama_exec, _semantic_search, _storage
from src.llm_velocity._service._look_up_store import _LookUpStore
from src.llm_velocity._engine import _tool_definition_store
from sentence_transformers import SentenceTransformer
from src.llm_velocity._models._models import ChatContext
from src.llm_velocity._constants import _constants
from src.llm_velocity._models import _models

class LLMLookUpStore:
    def __init__(self, ollama_model: str, ollama_url: str, tools_json_file_path: str):
        self.__storage_obj : _storage._Storage
        self.__ollama_model: str = ollama_model
        self.__ollama_url: str = ollama_url
        self.__tools_json_file_path: str = tools_json_file_path
        self.__database_exec_obj: _database_exec._DatabaseExec 
        self.__semantic_search_obj: _semantic_search._SemanticSearch
        self.__ollama_exec_obj: _ollama_exec._OllamaExec
        self.__tool_definition_store_obj: _tool_definition_store._ToolDefinitionStore
        self.__cache_manager_obj: _LookUpStore

    def init_setup(self) -> None:
        """Initial setup of class"""
        self.__storage_obj = _storage._Storage(_constants.PROJECT_NAME, _constants.DATABASE_NAME, _constants.INDEX_NAME)
        self.__database_exec_obj = _database_exec._DatabaseExec(self.__storage_obj.database_path)
        self.__ollama_exec_obj = _ollama_exec._OllamaExec(self.__ollama_url, self.__ollama_model)
        self.__semantic_search_obj = _semantic_search._SemanticSearch(SentenceTransformer(_constants.SENTENCE_TRANSORMER_MODEL), self.__storage_obj.index_path)
        self.__tool_definition_store_obj = _tool_definition_store._ToolDefinitionStore(self.__tools_json_file_path)
        self.__cache_manager_obj = _LookUpStore(self.__database_exec_obj, self.__semantic_search_obj, self.__ollama_exec_obj, self.__tool_definition_store_obj)

        self.__database_exec_obj.init_tables()
        self.__semantic_search_obj.load_index_from_file()
        self.__tool_definition_store_obj.load_tools()

    def call_store(self, chat_message: str) -> _models.StoreResp | None :
        look_up_store_res =  self.__cache_manager_obj.search_in_store(chat_message)
        if look_up_store_res != None:
            print("from store")
            return look_up_store_res

        ollama_call_res = self.__ollama_exec_obj.call(chat_message);

        if ollama_call_res != None:
            self.__cache_manager_obj.add_to_store(ChatContext(
                llm_response=ollama_call_res.llm_response,
                tool_name=ollama_call_res.tool_name,
                arguments=ollama_call_res.arguments,
                user_message=chat_message
            ))
            print("from ollama")
            return ollama_call_res

        return