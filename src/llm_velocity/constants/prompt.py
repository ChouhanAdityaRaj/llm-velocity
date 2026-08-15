EXTRACT_ARGUMENT: str = """You are a data extraction and validation assistant. Extract structured arguments from a multi-turn conversation.

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
Output: {{"tool_name": "book_flight", "llm_response": "Great, flying from Japan! Where would you like to go — New York or India?", "arguments": {{"flying_from": "Japan", "flying_to": null}}}}

Invalid + missing combined:
Args: "flying_from: china or japan", "flying_to: new york or india"
History: user_message: book a flight from india
Output: {{"tool_name": "book_flight", "llm_response": "We don't fly out of India — departures are only from China or Japan. We also only fly to New York or India. Which departure and destination would you like?", "arguments": {{"flying_from": null, "flying_to": null}}}}

Complete (multi-turn):
Args: "flying_from: china or japan", "flying_to: new york or india"
History:
user_message: book a flight from india
llm_response: We don't fly out of India — departures are only from China or Japan. We also only fly to New York or India. Which departure and destination would you like?
user_message: japan to india
Output: {{"tool_name": "book_flight", "llm_response": null, "arguments": {{"flying_from": "Japan", "flying_to": "India"}}}}

### OUTPUT SCHEMA:
{{
  "tool_name": "<inferred intent>",
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
IMPORTANT: You must format your final response STRICTLY as a valid JSON object. Do not include any text outside of the JSON structure. 

The JSON must exactly match the following structure:
{"tool_name": string | null, "llm_response": string | null, "arguments": object | null}

Follow these strict rules when constructing the JSON:
1. Tool Identification: If the user's request requires a tool, output its exact name in "tool_name". If no tool is needed, set to null.
2. Strict Schema Enforcement: You MUST include EVERY expected parameter for the chosen tool inside the "arguments" object. DO NOT omit any required keys, even if the user did not provide the data. 
3. Handling Missing Data: If the user provided the data for a parameter, extract and assign it. If the user did NOT provide data for an expected parameter, you MUST still include the key in the "arguments" object and set its value strictly to null.
4. Conversational Output & Answers: If there is ANY question, answer, or general information you need to communicate to the user, you MUST place it strictly inside the "llm_response" string. 
5. Mandatory Follow-up: Evaluate the "arguments" object. If ANY key has a value of null, you MUST write a conversational, user-friendly question in "llm_response" asking the user to provide that specific missing information. Do NOT set "llm_response" to null if there are null arguments.
6. Ready to Execute: ONLY if all expected arguments for a tool are fully populated with valid user data AND you have no other conversational answers/information to provide, set "llm_response" to null.

Examples of Expected Output:

Scenario: Tool requires 'flying_from' and 'flying_to'. User says: "Book a flight from China."
{"tool_name": "book_flight", "llm_response": "I can help with that! Where are you flying to from China?", "arguments": {"flying_from": "China", "flying_to": null}}

Scenario: Tool requires 'flying_from' and 'flying_to'. User says: "Book a flight from China to Japan."
{"tool_name": "book_flight", "llm_response": null, "arguments": {"flying_from": "China", "flying_to": "Japan"}}

Scenario: No tool is needed. User says: "What is the capital of France?"
{"tool_name": null, "llm_response": "The capital of France is Paris.", "arguments": null}
   """