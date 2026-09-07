EXTRACT_ARGUMENT: str = """
Extract argument values from the chat context below for each parameter listed. Use parameter description to identify correct value. If a parameter's value isn't found in context, use null.

Parameters:
{parameters}

Chat context:
{chat_context}

Rules:
- Match by meaning, not exact wording.
- Output ONLY the array, no explanation.
- Preserve parameter order.
- Use null if not found.

Output format:
[{{"param":"param_name_1","value":"<value or null>"}},{{"param":"param_name_2","value":"<value or null>"}}]
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