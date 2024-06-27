tools = {
      "type": "function",
      "function": {
        "name": "get_research",
        "description": "pass user query to research assistant, to retrieve data from vector store. return data as str, data organized in bullet point format",
        "parameters": {
          "type": "string",
          "properties": {
            "query": {
              "type": "string",
              "description": "a query that is a summary of critical information from the users original question"
            }
          },
          "required": ["query"]
        }
      }
    }