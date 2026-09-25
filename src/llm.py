import json
import urllib.request
from dataclasses import dataclass


@dataclass
class Response:
    """Structured response from the language model."""

    content: str = ""
    reasoning: str | None = None
    tool_call: dict | None = None
    metadata: dict | None = None


class LLM:
    """Interface for interacting with a language model."""

    def __init__(
        self,
        model: str,
        base_url: str = "http://127.0.0.1:8080",  # "http://localhost:11434/v1",
        api_key: str | None = None,
        think: bool = False,
    ):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.think = think

    def generate(
        self, messages: list[dict[str, str]], tools: list | None = None
    ) -> Response:
        """Generate a response from the language model based on the given prompt."""
        # build the request payload
        payload = {
            "model": self.model,
            "messages": messages,
        }

        # tools and reasoning
        if tools is not None:
            payload["tools"] = tools

        if not self.think:
            payload["reasoning"] = "none"

        # print(f"Request payload: {payload}")

        # POST to the OpenAI-compatible /chat/completions endpoint
        request = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}),
            },
        )

        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            # print(f"Response JSON: {json.dumps(response_json, indent=4)}")

        # Extract messages, tool_calls and metadata from the response JSON.
        message = response_json["choices"][0]["message"]
        tool_calls = message.get("tool_calls", [])
        tool_call = tool_calls[0] if tool_calls else None
        metadata = {
            "model": response_json.get("model", None),
            "prompt_tokens": response_json.get("usage", {}).get("prompt_tokens", None),
            "completion_tokens": response_json.get("usage", {}).get(
                "completion_tokens", None
            ),
            "total_tokens": response_json.get("usage", {}).get("total_tokens", None),
        }

        # format as a Response object
        return Response(
            content=message.get("content", ""),
            reasoning=message.get("reasoning", None),
            tool_call=tool_call,
            metadata=metadata,
        )
