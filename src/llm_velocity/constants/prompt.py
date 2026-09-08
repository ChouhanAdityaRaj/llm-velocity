EXTRACT_ARGUMENT: str = """
Extract each parameter value from CHAT using its name/description.

Rules:
1. Use only explicitly stated or clearly resolved information.
2. Never infer, guess, default, or use outside knowledge.
3. Missing/ambiguous/incomplete value → null.
4. On corrections, use the latest user value.
5. Match semantically.
6. Keep exact parameter names and order; include every parameter once.
7. Output ONLY valid JSON, no markdown or explanation.

PARAMETERS:
{parameters}

CHAT:
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