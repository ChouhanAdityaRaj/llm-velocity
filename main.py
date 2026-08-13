from llm_velocity import LLMLookUpStore

prompt = """
You are a flight booking assistant. Your only job is to extract `flying_from` and `flying_to`.

Available tool:

book_flight(
    flying_from: string,
    flying_to: string
)

Rules:
1. If both cities are explicitly provided, output ONLY valid, raw JSON (no markdown, no text):
   {"tool_name": "book_flight", "flying_from": "<city>", "flying_to": "<city>"}
2. If any required information is missing, reply ONLY with a brief question asking for it. 
3. Never guess or invent city names. 
4. Remember previously collected cities and update them if the user changes their mind.

user_message: book a flight from china

"""

luStore = LLMLookUpStore("llama3.2:3b","http://localhost:11434", "data_collection/tool.json")

luStore.init_setup()

res = luStore.call_store(prompt)
print(res)