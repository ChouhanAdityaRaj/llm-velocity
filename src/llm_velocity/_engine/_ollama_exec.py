import json
import requests
from src.llm_velocity._constants import _constants, _prompt
from src.llm_velocity._models import _models

class _OllamaExec:
    def __init__(self, ollama_host: str, ollama_model: str):
        self.__ollama_url: str = f"{ollama_host}/api/chat"
        self.__ollama_model: str = ollama_model

    def  extract_argument(self, user_message: str, argument_to_extract: list[str]) -> tuple[str, dict[str: str]]:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """

        exteracted_user_ai_chat_msg = user_message[user_message.find(_constants.USER_MESSAGE_PROPERTY):]
        
        response = requests.post(self.__ollama_url, json={
            "model": self.__ollama_model,
            "messages": [
                {
                    "role": "user",
                    "content": _prompt.EXTRACT_ARGUMENT.format(user_message=exteracted_user_ai_chat_msg, argument_to_extract=argument_to_extract)
                }
            ],
            "stream": False,
            "format": "json"
        }, timeout=60)

        data = response.json()

        try:

            resp = json.loads(data["message"]["content"])
            return resp["llm_response"], resp["arguments"]
        except Exception:
            print("RAW OUTPUT:", data)
            return None
        
    def  call(self, user_prompt: str) -> _models.StoreResp | None:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """
        
        response = requests.post(
            self.__ollama_url,
            json={
                "model": self.__ollama_model,
                "messages": [
                    {
                        "role": "user",
                        "content": f"{user_prompt}\n{_prompt.LLM_SUFFIX}"
                    }
                ],
                "stream": False,
                "format": "json"
            },
            timeout=600
        )

        data = response.json()

        try:
            # json_llm_resp = json.loads(data["response"]) # generate
            json_llm_resp = json.loads(data["message"]["content"]) #chat
            return _models.StoreResp(**json_llm_resp)
        except Exception:
            print("RAW OUTPUT:", data)
            return None
    
        