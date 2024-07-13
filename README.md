# GAim Bot
Pair of AI agents that use RAG for answering user questions about the game Eldin Ring. The underlying architecture works for any game, it just depends on the information provided to the research model. This works as an alternative to videogame guides or wikis as it can provide
- custom responses based on quiery powered by gpt-4o
- ability to synethesize information that would traditionally be contained across a number of wiki pages
- ability to give hints or avoid spoilers in the answer upon the user's request

How it Works
- The front end is powered by streamlit, to create a basic chatbot interface
- Conversation Bot: After a user query, the query is sent to a gpt-4o model which then creates a simplified query
- Research Bot: this bot is called by the conversation bot. It has a vector store of releveant information for a particular game. It creates a bullet point summary of relevant points and returns said information to the Conversation bot to give to the user
- Why this architecture?
    - GPT-4o is the current OpenAI flagship model. It has noticeably superior conversational ability to gpt-3, and in testing gave far better responses to query's on game infromation
    - the cost of gpt-4o is however 2500 times more expensive, and RAG can greatly increase the number of tokens used per query
    - The Solution: GPT-40 is used to converse with the user and enhance their experience, however through the assistants api the GPT-4o model uses GPT-3 to perform RAG at lower cost and then summarizes the results to the user
    - this does result in increased latency per request, however the tradeoff makes the application much more finanically viable as a hobby project per request
