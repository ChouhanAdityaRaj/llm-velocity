import requests


def call_llm(
    provider: str,
    prompt: str,
    model: str = None,
    system: str = None,
    temperature: float = 1.0,
    api_key: str = None,
    timeout: int = 600,
) -> str:
    provider = provider.lower()

    if provider == "anthropic":
        return _call_anthropic(prompt, model, system, temperature, api_key, timeout)
    elif provider == "openai":
        return _call_openai(prompt, model, system, temperature, api_key, timeout)
    elif provider == "gemini":
        return _call_gemini(prompt, model, system, temperature, api_key, timeout)
    elif provider == "ollama":
        return _call_gemini(prompt, model, system, temperature, api_key, timeout)
    else:
        raise ValueError(f"Unsupported provider: {provider!r}. Use 'anthropic', 'openai', or 'gemini'.")
