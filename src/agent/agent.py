from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from src.agent.client import ClaudeClient
from src.agent.tools import ALL_TOOLS
from src.eval.graders.base import ToolCallRecord
from src.wikipedia.retriever import fetch_page_content, search_pages

_PROMPTS_DIR = Path(__file__).parent / "prompts"
_MAX_TOOL_ROUNDS = 6  # safety cap on agentic back-and-forth turns


def _latest_prompt_version() -> str:
    versions = sorted(_PROMPTS_DIR.glob("v*.md"), key=lambda p: int(p.stem[1:]))
    if not versions:
        raise FileNotFoundError(f"No prompt files found in {_PROMPTS_DIR}")
    return versions[-1].stem  # e.g. "v1"


def load_prompt(version: str | None = None) -> tuple[str, str]:
    """Return (version_label, prompt_text). Defaults to latest."""
    ver = version or _latest_prompt_version()
    path = _PROMPTS_DIR / f"{ver}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return ver, path.read_text()


@dataclass
class AgentResult:
    output: str
    conversation: list[dict]
    tool_calls: list[ToolCallRecord]
    prompt_version: str
    model: str
    latency_ms: int
    total_tool_calls: int
    error: str | None = None


def run(
    question: str,
    client: ClaudeClient,
    prompt_version: str | None = None,
) -> AgentResult:
    """Run the agentic question-answering loop and return a full AgentResult."""
    ver, system_prompt = load_prompt(prompt_version)
    messages: list[dict] = [{"role": "user", "content": question}]
    tool_call_records: list[ToolCallRecord] = []
    call_index = 0
    t0 = time.monotonic()

    try:
        for _ in range(_MAX_TOOL_ROUNDS):
            response = client.complete(
                system=system_prompt,
                messages=messages,
                tools=ALL_TOOLS,
            )

            if response["tool_calls"]:
                messages.append({
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": tc["id"],
                            "name": tc["name"],
                            "input": tc["input"],
                        }
                        for tc in response["tool_calls"]
                    ],
                })
            else:
                messages.append({
                    "role": "assistant",
                    "content": response["content"] or "",
                })

            if not response["tool_calls"]:
                break

            tool_results = []
            for tc in response["tool_calls"]:
                query = tc["input"].get("query", "")
                api_response = search_pages(query, limit=5)

                fetched_content = ""
                content_source = "none"
                if api_response:
                    top_key = api_response[0].get("key", "")
                    if top_key:
                        fetched_content = fetch_page_content(top_key)
                        content_source = f"page/{top_key}/with_html (stripped)"

                tool_call_records.append(ToolCallRecord(
                    call_index=call_index,
                    query=query,
                    api_response={"pages": api_response},
                    fetched_content=fetched_content,
                    content_source=content_source,
                ))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tc["id"],
                    "content": fetched_content or "No relevant Wikipedia content found.",
                })
                call_index += 1

            messages.append({"role": "user", "content": tool_results})

        latency_ms = int((time.monotonic() - t0) * 1000)

        return AgentResult(
            output=response.get("content") or "",
            conversation=messages,
            tool_calls=tool_call_records,
            prompt_version=ver,
            model=client.model,
            latency_ms=latency_ms,
            total_tool_calls=len(tool_call_records),
        )

    except Exception as exc:  # noqa: BLE001
        latency_ms = int((time.monotonic() - t0) * 1000)
        return AgentResult(
            output="",
            conversation=messages,
            tool_calls=tool_call_records,
            prompt_version=ver,
            model=client.model,
            latency_ms=latency_ms,
            total_tool_calls=len(tool_call_records),
            error=str(exc),
        )
