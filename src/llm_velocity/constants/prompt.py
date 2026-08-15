EXTRACT_ARGUMENT: str = """
You are a data extraction and validation assistant. Extract structured arguments from a multi-turn conversation.

### RULES:
1. Read the full history; later user messages override earlier ones for the same field, but valid values from earlier turns still count if never contradicted.
2. Validate every value against its constraint.
3. If a value is missing OR invalid, set it to null. Never invent or substitute a value the user didn't provide.
4. If any argument is null:
   - Write one natural, cohesive "llm_response" that: acknowledges any newly-provided valid info, notes any invalid input given (state why it's invalid), and asks for all still-missing/invalid fields together with their valid options — as a single question, not several robotic ones.
   - Do not repeat prior assistant messages.
5. If all arguments are valid, set "llm_response" to null.
6. Output strictly valid JSON only — no markdown, no extra text.

### EXAMPLES:

Missing value:
Args: "flying_from: china or japan", "flying_to: new york or india"
History: user_message: I want to book a flight from Japan.
Output: {{"llm_response": "Great, flying from Japan! Where would you like to go — New York or India?", "arguments": {{"flying_from": "Japan", "flying_to": null}}}}

Invalid + missing combined:
Args: "flying_from: china or japan", "flying_to: new york or india"
History: user_message: book a flight from india
Output: {{"llm_response": "We don't fly out of India — departures are only from China or Japan. We also only fly to New York or India. Which departure and destination would you like?", "arguments": {{"flying_from": null, "flying_to": null}}}}

Complete (multi-turn):
Args: "flying_from: china or japan", "flying_to: new york or india"
History:
user_message: book a flight from india
llm_response: We don't fly out of India — departures are only from China or Japan. We also only fly to New York or India. Which departure and destination would you like?
user_message: japan to india
Output: {{"llm_response": null, "arguments": {{"flying_from": "Japan", "flying_to": "India"}}}}

### OUTPUT SCHEMA:
{{
  "llm_response": "<unified follow-up question or null>",
  "arguments": {{
    "<key_name>": "<valid_value_or_null>"
  }}
}}

### ARGUMENTS & CONSTRAINTS:
{argument_to_extract}

### CONVERSATION HISTORY:
{conversation_history}
"""

LLM_SUFFIX: str = """
IMPORTANT: Respond STRICTLY as valid JSON, no text outside it, matching:
{"tool_name": string | null, "llm_response": string | null, "arguments": object | null}

Rules:
1. "tool_name": exact tool name if one is needed, else null.
2. If a tool is used, "arguments" MUST include every expected parameter as a key — never omit one. Fill in values the user gave; set any not given to null.
3. Put all conversational text (questions, answers, info) in "llm_response" — never elsewhere.
4. If any argument is null, "llm_response" MUST ask the user for that missing info (never null in this case).
5. Set "llm_response" to null ONLY if all arguments are filled AND you have nothing else to say. If no tool is needed, set "arguments" to null.

Examples:

User: "Book a flight from China." (tool needs flying_from, flying_to)
{"tool_name": "book_flight", "llm_response": "I can help with that! Where are you flying to from China?", "arguments": {"flying_from": "China", "flying_to": null}}

User: "Book a flight from China to Japan." (tool needs flying_from, flying_to)
{"tool_name": "book_flight", "llm_response": null, "arguments": {"flying_from": "China", "flying_to": "Japan"}}

User: "What is the capital of France?" (no tool needed)
{"tool_name": null, "llm_response": "The capital of France is Paris.", "arguments": null}
   """