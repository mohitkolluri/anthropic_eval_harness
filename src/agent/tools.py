SEARCH_WIKIPEDIA_TOOL = {
    "name": "search_wikipedia",
    "description": (
        "Search or fetch Wikipedia content. Use action='search' to find candidate articles "
        "by entity name — returns a ranked list of candidates with key, title, description, and excerpt. "
        "Use action='fetch' to retrieve the full content of a specific article using its page key "
        "from a previous search result. Always search first, then fetch the chosen candidate."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["search", "fetch"],
                "description": (
                    "'search' — find candidate articles by entity name. "
                    "'fetch' — retrieve full content of a specific article by its page key."
                ),
            },
            "query": {
                "type": "string",
                "description": (
                    "For action='search': an entity name or Wikipedia article title (noun phrase, not a question). "
                    "For action='fetch': the exact page key returned by a previous search "
                    "(e.g. 'Jaguar', 'Jaguar_Cars', 'Mercury_(planet)')."
                ),
            },
        },
        "required": ["action", "query"],
    },
}

ALL_TOOLS: list[dict] = [SEARCH_WIKIPEDIA_TOOL]
