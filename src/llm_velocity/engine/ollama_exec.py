import json
import requests
from src.llm_velocity.constants import prompt, constants
from src.llm_velocity.models import models

class OllamaExec:
    def __init__(self, ollama_host: str, ollama_model: str):
        self.__ollama_url: str = f"{ollama_host}/api/chat"
        self.__ollama_model: str = ollama_model

    def  extract_argument(self, user_message: str, argument_to_extract: list[str]) -> tuple[str, dict[str: str]]:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """

        exteracted_user_ai_chat_msg = user_message[user_message.find(constants.USER_MESSAGE_PROPERTY):]
        
        response = requests.post(self.__ollama_url, json={
            "model": self.__ollama_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt.EXTRACT_ARGUMENT.format(conversation_history=exteracted_user_ai_chat_msg, argument_to_extract=", ".join(argument_to_extract))
                }
            ],
            "stream": False,
            "format": "json"
        }, timeout=600)

        data = response.json()

        try:

            resp = json.loads(data["message"]["content"])
            return resp["llm_response"], resp["arguments"]
        except Exception:
            # print("RAW OUTPUT:", data)
            return models.StoreResp(error="internal error")
        
    def  call(self, user_prompt: str) -> models.StoreResp | None:
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
                        "content": f"{user_prompt}\n{prompt.LLM_SUFFIX}"
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
            return models.StoreResp(**json_llm_resp)
        except Exception:
            # print("RAW OUTPUT:", data)
            return models.StoreResp(error="internal error")
    
        