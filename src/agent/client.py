from __future__ import annotations

import os

import anthropic

_DEFAULT_MODEL = "claude-haiku-4-5-20251001"


class ClaudeClient:
    def __init__(self, model: str = _DEFAULT_MODEL) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        self.model = model
        self._client = anthropic.Anthropic(api_key=api_key)

    def complete(
        self,
        system: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        max_tokens: int = 1024,
    ) -> dict:
        """
        Call the Claude API and return a normalised dict:
          content    (str | None)   — final text response
          tool_calls (list[dict])   — [{id, name, input}]
          stop_reason (str)
        """
        kwargs: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = self._client.messages.create(**kwargs)

        content: str | None = None
        tool_calls: list[dict] = []

        for block in response.content:
            if isinstance(block, anthropic.types.TextBlock):
                content = block.text
            elif isinstance(block, anthropic.types.ToolUseBlock):
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        return {
            "content": content,
            "tool_calls": tool_calls,
            "stop_reason": response.stop_reason,
        }
