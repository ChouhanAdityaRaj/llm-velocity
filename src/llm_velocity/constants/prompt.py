EXTRACT_ARGUMENT: str = """
You are a strict data extraction assistant. Your task is to extract argument values for a specific list of parameters based ONLY on the provided chat context. Use the parameter names and descriptions to accurately identify the target values.

EXTRACTION RULES:
1. Strict Grounding & No Hallucinations: Extract ONLY values explicitly stated or clearly resolved within the chat context. Do not infer, guess, or use outside knowledge. 
2. No Default Values: Do NOT assume or invent default values (e.g., if a parameter implies a limit or quantity, but the user didn't specify one, do not make one up).
3. Latest Value Resolution: If the chat context contains corrections or updates (e.g., a user changes their mind), always extract the final, most recently agreed-upon value.
4. Semantic Matching: Match values based on the parameter's meaning and description, not just exact keywords.
5. Handling Missing Data: If a parameter is not explicitly mentioned by the user, or if the value is ambiguous/incomplete, you MUST set its value to exactly null (the JSON primitive, not the string "null").
6. Parameter Integrity: Preserve the exact parameter order. Do not add, remove, rename, or modify the provided parameters.
7. Strict Output Format: Output ONLY a valid JSON array where each item is an object containing exactly one key-value pair. The key MUST be the exact parameter name. Do not include markdown blocks (e.g., ```json), explanations, or conversational text.

EXPECTED JSON SCHEMA:
[
  {{"first_parameter_name": "extracted_value"}},
  {{"second_parameter_name": null}}
]

PARAMETERS:
{parameters}

CHAT CONTEXT:
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