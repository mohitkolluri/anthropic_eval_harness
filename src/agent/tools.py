SEARCH_WIKIPEDIA_TOOL = {
    "name": "search_wikipedia",
    "description": (
        "Search Wikipedia by entity name or article title to retrieve factual information. "
        "The query must be a named entity (person, place, event, concept, organisation) — "
        "not a rephrased version of the question. "
        "Good: 'Mount Everest', 'Hundred Years War', 'Boiling point'. "
        "Bad: 'boiling point of water at Everest', 'how long did the Hundred Years War last'."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A Wikipedia article title or named entity. Must be a noun phrase, not a question or sentence.",
            }
        },
        "required": ["query"],
    },
}

ALL_TOOLS: list[dict] = [SEARCH_WIKIPEDIA_TOOL]
