SEARCH_WIKIPEDIA_TOOL = {
    "name": "search_wikipedia",
    "description": (
        "Search Wikipedia to find factual information about a topic. "
        "Use this for any question that requires factual knowledge. "
        "Returns a summary of the most relevant Wikipedia article."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Be specific — use key terms, names, or titles rather than full questions.",
            }
        },
        "required": ["query"],
    },
}

ALL_TOOLS: list[dict] = [SEARCH_WIKIPEDIA_TOOL]
