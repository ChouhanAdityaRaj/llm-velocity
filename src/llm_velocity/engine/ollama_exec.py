import json
import requests
from src.llm_velocity.constants import prompt, constants
from src.llm_velocity.models import models
from dataclasses import fields

class OllamaExec:
    def __init__(self, ollama_host: str, ollama_model: str):
        self.__ollama_url: str = f"{ollama_host}/api/chat"
        self.__ollama_model: str = ollama_model

    def  extract_argument(self, chat_context: list[models.UserChatReq], argument_to_extract: list[dict[str, str]]) ->  list[dict[str, str]]:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """

        formatted_chat_context =  "\n".join(
            f"{field.name}: {getattr(chat, field.name)}"
            for chat in chat_context
            for field in fields(chat)
        )

        formatted_parameters = "\n".join(f"{k}: {v}" for k, v in argument_to_extract.items())

        print("Prompt: ", prompt.EXTRACT_ARGUMENT.format(chat_context=formatted_chat_context, parameters=formatted_parameters),)
        
        response = requests.post(self.__ollama_url, json={
            "model": self.__ollama_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt.EXTRACT_ARGUMENT.format(chat_context=formatted_chat_context, parameters=formatted_parameters),
                }
            ],
            "stream": False,
            "format": "json"
        }, timeout=600)

        data = response.json()

        resp: list[dict[str, str | None]]  = list(data["message"]["content"])
        return resp
        
    def  call(self, user_prompt: str) -> str | None:
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

        res: str = data["message"]["content"]

        
        return None if res.strip() == "" else res

    
        