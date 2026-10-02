EXTRACT_ARGUMENT: str = """
Extract values for the keys in PARAMETERS from CHAT only.

Rules:
- Output one flat, valid JSON object using exactly the PARAMETERS keys, in order. No added, removed, renamed, or invented keys. No markdown, comments, or extra text.
- Match values to keys by meaning (name + description). Ignore unrelated chat content.
- Fill a value only if explicitly stated or unambiguously resolved. Never guess, infer, calculate, or default; if missing, unclear, or partial → null.
- If the user corrects a value later, use the latest one.
- Keep the user's wording exactly. Don't paraphrase or complete partial values.

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