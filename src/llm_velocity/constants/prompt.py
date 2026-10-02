EXTRACT_ARGUMENT: str = """
    Extract values ONLY for the parameters listed in PARAMETERS, using CHAT as the sole source.
    
    Rules:
    1. PARAMETERS is the full, exclusive list of keys to output — same names, same order.
    2. Never add, remove, rename, or invent keys.
    3. Fill a value only if explicitly stated or unambiguously resolved in CHAT.
    4. Never guess, infer, calculate, or default. If unclear/missing/partial → null.
    5. If the user later corrects a value, use the latest one.
    6. Match values to parameters by semantic meaning (name + description).
    7. Ignore CHAT content unrelated to the given parameters.
    8. Preserve user wording/meaning exactly — no paraphrasing or completing partial values.
    9. Output strictly valid JSON: one flat object, exact keys, no markdown/comments/extra text.
    
    PARAMETERS:
    {parameters}
    
    {chat_context}
"""

LLM_SUFFIX: str = """
    IMPORTANT: Respond STRICTLY as valid JSON, no text outside it, matching:
    {"tool_name": string | null, "llm_response": string | null, "arguments": object | null}
    
    Rules:
    1. "tool_name": exact tool name if one is needed, else null.
    2. If a tool is used, "arguments" MUST include every expected parameter as a key — never omit one. Fill in values the user gave; set any not given to null.
    3. Put all conversational text (questions, answers, info) in "llm_response" — never elsewhere.
    
    Examples:
    User: "Book a flight from China." (tool needs flying_from, flying_to)
    {"tool_name": "book_flight", "llm_response": "I can help with that! Where are you flying to from China?", "arguments": {"flying_from": "China", "flying_to": null}}
  """