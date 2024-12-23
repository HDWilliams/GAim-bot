tools=[
    {
      "type": "function",
      "function": {
        "name": "get_research",
        "description": "call bot to research topic of user query",
        "parameters": {
            "type": "object",
            "properties": {
            "query": {
                "type": "string",
                "description": "specific query related to eldin ring game"
            }
            },
            "required": [
            "query"
            ]
            }
        }
    },
    
]