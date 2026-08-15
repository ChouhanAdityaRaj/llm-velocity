EXTRACT_ARGUMENT: str = """You are an expert data extraction and validation assistant. Your task is to analyze a conversation and extract structured data based on specific rules.

### ARGUMENTS TO EXTRACT & CONSTRAINTS:
{argument_to_extract}

### CONVERSATION:
{user_message}

### INSTRUCTIONS:
1. Analyze the CONVERSATION and extract values for every key listed in the ARGUMENTS TO EXTRACT.
2. Validate each extracted value strictly against its corresponding constraint.
3. Map valid values to their keys in the "arguments" object.
4. MISSING OR INVALID VALUES (ANTI-HALLUCINATION): 
   - If a value is missing from the conversation, set it to null.
   - If the user provides a value that violates the validation constraint (e.g., an unsupported location), you MUST set its value to null. 
   - NEVER substitute an invalid or missing value with a random valid value. Only extract exactly what the user provides.
5. GENERATING LLM_RESPONSE (CRITICAL): 
   - If ANY value in "arguments" is null, you MUST write a polite, user-friendly question in "llm_response" asking the user to provide or correct that specific information. 
   - If the user provided an invalid value, acknowledge what they asked for, politely inform them it is not an option, and explicitly state the allowed options based on the constraints.
   - If multiple values are missing/invalid, do not ask multiple robotic questions back-to-back. Instead, blend the missing information naturally into a single, cohesive conversational response that states the available options for all missing fields and asks one unified question.
   - If ALL values in "arguments" are valid and present, set "llm_response" to null.
6. Output strictly valid JSON. Do not include markdown formatting (like ```json), explanations, or any text outside the JSON object.
-
### EXAMPLES:

Example 1 (Missing Value):
Arguments: "flying_from: can only be china or japan", "flying_to: can only be new york or india"
Conversation: "I want to book a flight from Japan."
Output:
{{
  "tool_name": "book_flight",
  "llm_response": "I can certainly help you book a flight from Japan! Where would you like to fly to? Our current destinations are New York or India.",
  "arguments": {{
    "flying_from": "Japan",
    "flying_to": null
  }}
}}

Example 2 (Invalid Value Provided):
Arguments: "flying_from: can only be china or japan", "flying_to: can only be new york or india"
Conversation: "Get me a ticket from Germany to New York"
Output:
{{
  "tool_name": "book_flight",
  "llm_response": "I see you want to fly to New York, but unfortunately, we do not have flights departing from Germany. We currently only offer departures from China or Japan. Which of these would you prefer to fly from?",
  "arguments": {{
    "flying_from": null,
    "flying_to": "New York"
  }}
}}

Example 3 (All Values Correct):
Arguments: "flying_from: can only be china or japan", "flying_to: can only be new york or india"
Conversation: "Get me a ticket from China to New York"
Output:
{{
  "tool_name": "book_flight",
  "llm_response": null,
  "arguments": {{
    "flying_from": "China",
    "flying_to": "New York"
  }}
}}

Example 4 (Invalid Value AND Missing Value):
Arguments: "flying_from: can only be china or japan", "flying_to: can only be new york or india"
Conversation: "book a flight from india"
Output:
{{
  "tool_name": "book_flight",
  "llm_response": "I can certainly help you book a flight! However, we currently don't offer departures from India; our departure locations are limited to China or Japan. We also only fly to New York or India. Could you let me know your preferred departure and destination from these options?",
  "arguments": {{
    "flying_from": null,
    "flying_to": null
  }}
}}

### JSON OUTPUT SCHEMA:
{{
  "tool_name": "<infer the intent/tool name from context>",
  "llm_response": "<string with a unified follow-up question including valid options, or null if all arguments are filled>",
  "arguments": {{
    "<key_name>": "<valid_value or null>"
  }}
}}"""

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