import json
import requests
from src.llm_caching.constants import prompt

class OllamaExec:
    def __init__(self, ollama_host: str, ollama_model: str):
        self.__ollama_url: str = f"{ollama_host}/api/generate"
        self.__ollama_model: str = ollama_model

    def  extract_argument(self, user_message: str, argument_to_extract: list[str]) -> dict[str: str]:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """
        
        response = requests.post(self.__ollama_url, json={
            "model": self.__ollama_model,
            "prompt": prompt.EXTRACT_ARGUMENT.format(user_message=user_message, argument_to_extract=argument_to_extract),
            "stream": False,
            "format": "json"
        }, timeout=60)

        data = response.json()

        try:
            return json.loads(data["response"])
        except Exception:
            print("RAW OUTPUT:", data)
            return None
        
    def  call(self, prompt: str):
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """
        
        response = requests.post(self.__ollama_url, json={
            "model": self.__ollama_model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }, timeout=60)

        data = response.json()

        try:
            return json.loads(data["response"])
        except Exception:
            print("RAW OUTPUT:", data)
            return None
    
        