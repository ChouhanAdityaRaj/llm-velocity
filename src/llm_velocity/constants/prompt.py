EXTRACT_ARGUMENT: str = """
      You extract arguments from a user message.
      Extract the value for each label listed below.

      Rules:
      - Return ONLY valid JSON.
      - Use exactly the provided labels as JSON keys.
      - Use only information explicitly stated in the user message.
      - Do not infer, guess, transform, or generate values.
      - If a value is not explicitly present, return null.
      - Preserve the value as stated by the user.
      - Do not add extra keys.

      User message:
      {user_message}

      Labels:
      {argument_to_extract}
   """

LLM_SUFFIX: str = """
You are a routing agent. Output ONLY valid raw JSON. No markdown or extra text.

ALWAYS return exactly this structure:
{
"tool_name": string | null,
"llm_response": string | null,
"arguments": {}
}

RULES:

1. If a tool is required:

   * "tool_name" = tool name
   * "llm_response" = null
   * ALL tool parameters MUST be inside "arguments".
2. If no tool is required:

   * "tool_name" = null
   * "llm_response" = response
   * "arguments" = {}
3. NEVER put parameters at the root.
4. NEVER omit or rename any key.
5. Use valid JSON with double quotes.

Example:
User: "Book flight from Mumbai to Delhi"

{
"tool_name": "reserce_flight",
"llm_response": null,
"arguments": {
"from_city": "Mumbai",
"to_city": "Delhi"
}
}

"""