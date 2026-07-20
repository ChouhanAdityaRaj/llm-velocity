from src.LLMVelocity.api.llm_look_up_store import LLMLookUpStore

luStore = LLMLookUpStore("phi3:mini","http://localhost:11434", "E:\Projects\Major Project\LLM Caching\data_collection\tool.json")

luStore.init_setup()

while True:
    prompt = input("Prompt: ")

    res = luStore.call_store(prompt)
    print(res)

