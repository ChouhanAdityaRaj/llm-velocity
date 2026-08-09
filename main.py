from src.llm_velocity.api.llm_look_up_store import LLMLookUpStore

# luStore = LLMLookUpStore("phi3:mini","http://localhost:11434", "E:\Projects\Major Project\LLM Caching\data_collection\tool.json")

# luStore.init_setup()

# while True:
#     prompt = input("Prompt: ")

#     res = luStore.call_store(prompt)
#     print(res)

from src.llm_velocity.engine.ollama_exec import OllamaExec
# obj = OllamaExec("http://localhost:11434","llama3.2:3b" )

prompt = """
You are a flight booking assistant. Your only job is to extract `from_city` and `to_city`.

Available tool:

book_flight(
    from_city: string,
    to_city: string
)

Rules:
1. If both cities are explicitly provided, output ONLY valid, raw JSON (no markdown, no text):
   {"tool_name": "book_flight", "from_city": "<city>", "to_city": "<city>"}
2. If any required information is missing, reply ONLY with a brief question asking for it. 
3. Never guess or invent city names. 
4. Remember previously collected cities and update them if the user changes their mind.

user_message: book a flight from udaipur
"""

# res = obj.call(prompt)
# print(res)

luStore = LLMLookUpStore("llama3.2:3b","http://localhost:11434", "data_collection/tool.json")

luStore.init_setup()

res = luStore.call_store(prompt)
print(res)