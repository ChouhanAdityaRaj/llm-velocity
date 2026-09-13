import json
import requests
from src.llm_velocity.constants import prompt, constants
from src.llm_velocity.models import models
from dataclasses import fields
from typing import Any 

class LLMExec:
    def __init__(self,llm_provider: str, llm_host: str, llm_model: str, api_key: str, temperature: float=0.7):
        self.__llm_url: str = f"{llm_host}/api/chat"
        self.__llm_model: str = llm_model
        self.__api_key: str = api_key
        self.__temperature: float = temperature
        self.__llm_provider: models.LlmProvider = models.LlmProvider(llm_provider)

    def  extract_argument(self, chat_context: list[models.UserChatReq], argument_to_extract: list[tuple[str, str]]) ->  dict[str, Any]:
        """ 
            Method to extract argument from user message based on provided argument labels. 
            return 
        """

        formatted_chat_context = "\n".join(
            f"{field.name}: {getattr(chat, field.name)}"
            for chat in chat_context
            for field in fields(chat)
            if getattr(chat, field.name) is not None
        )

        formatted_parameters = "\n".join(f"{key}: {value}" for key, value in argument_to_extract)

        print("Prompt: ", prompt.EXTRACT_ARGUMENT.format(chat_context=formatted_chat_context, parameters=formatted_parameters))

        data = None

        match self.__llm_provider:
            case models.LlmProvider.ANTHROPIC:
                data = self.__call_anthropic(formatted_chat_context, prompt.EXTRACT_ARGUMENT.format(chat_context=None, parameters=formatted_parameters))
            case models.LlmProvider.OPENAI:
                data = self.__call_openai(formatted_chat_context, prompt.EXTRACT_ARGUMENT.format(chat_context=None, parameters=formatted_parameters))
            case models.LlmProvider.GEMINI:
                data = self.__call_gemini(formatted_chat_context, prompt.EXTRACT_ARGUMENT.format(chat_context=None, parameters=formatted_parameters))
            case models.LlmProvider.OLLAMA:
                data = self.__call_ollama(prompt.EXTRACT_ARGUMENT.format(chat_context=formatted_chat_context, parameters=formatted_parameters))



        if not data:
            return {}
        
        data = data.strip()

        if data.startswith("```"):
            data = data.removeprefix("```json").removeprefix("```")
            data = data.removesuffix("```").strip()
        
        resp: dict[str, Any] = json.loads(data)
        return resp
        
    def  call(self, user_prompt: str) -> str | None:
        return self.__call_llm(f"{user_prompt}\n{prompt.LLM_SUFFIX}")


    ##### Internal methods


    def __call_anthropic(self, prompt: str, system: str =None):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.__api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model":  self.__llm_model,
            "max_tokens": 4096,
            "temperature": self.__temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        resp = requests.post(url, headers=headers, json=payload, timeout=constants.DEFAULT_LLM_TIME_OUT)
        resp.raise_for_status()
        data = resp.json()
        return "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")


    def __call_openai(self, prompt: str, system: str =None):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model":  self.__llm_model,
            "messages": messages,
            "temperature": self.__temperature,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=constants.DEFAULT_LLM_TIME_OUT)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


    def __call_gemini(self, prompt: str, system: str =None):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.__llm_model}:generateContent?key={self.__api_key}"
        headers = {"Content-Type": "application/json"}

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.__temperature,
            },
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}

        resp = requests.post(url, headers=headers, json=payload, timeout=constants.DEFAULT_LLM_TIME_OUT)
        resp.raise_for_status()
        data = resp.json()
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)

    def __call_ollama(self, prompt: str):
        response = requests.post(self.__llm_url, json={
            "model": self.__llm_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
            "format": "json"
        }, timeout=constants.DEFAULT_LLM_TIME_OUT)

        data = response.json()

        return data["message"]["content"]


        