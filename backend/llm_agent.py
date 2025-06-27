import os


class LLMAgent:
    """Simple OpenAI API wrapper."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def ask(self, prompt: str, mode: str = "default") -> str:
        """Send a prompt to the OpenAI API and return the response."""
        try:
            import openai  # type: ignore
        except Exception as exc:  # pragma: no cover - library not installed
            raise RuntimeError("openai package not available") from exc

        client = openai.OpenAI(api_key=self.api_key)
        messages = [{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            model=self.model, messages=messages
        )
        return completion.choices[0].message.content.strip()
