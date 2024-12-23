# GAim Bot
https://gaim-bot.streamlit.app

Pair of AI agents that use RAG for answering user questions about the game Eldin Ring. The underlying architecture works for any game, it just depends on the information provided to the research model. This works as an alternative to videogame guides or wikis as it can provide
- custom responses based on quiery powered by gpt-4o
- ability to synethesize information that would traditionally be contained across a number of wiki pages
- ability to give hints or avoid spoilers in the answer upon the user's request
- persistent conversation powered by assistants API allows users to ask follow up questions, of for progressive hints

How to Run It
1. Git clone https://github.com/HDWilliams/GAim-bot
2. Optional: set up virtual env in VS Code
3. pip install -r requirements.txt
4. Rename secrets_CLONED._toml to secrets.toml and populate with GPT OPEN AI key
5. Optional ASSISTANT_ID can be used to retrieve an existing assistant, by default new assistant is created
6. Run with: streamlit run GAimBot.py
7. Models for research and conversation can be updated in secrets.toml file

How it Works
- The front end is powered by streamlit, to create a basic chatbot interface
- Conversation Bot: After a user query, the query is sent to a gpt-4o model which then creates a simplified query
- Research Bot: this bot is called by the conversation bot. It has a vector store of releveant information for a particular game. It creates a bullet point summary of relevant points and returns said information to the Conversation bot to give to the user
- Why this architecture?
    - GPT-4o is the current OpenAI flagship model. It has noticeably superior conversational ability to gpt-3, and in testing gave far better responses to query's on game infromation
    - the cost of gpt-4o is however 2500 times more expensive, and RAG can greatly increase the number of tokens used per query
    - The Solution: GPT-40 is used to converse with the user and enhance their experience, however through the assistants api the GPT-4o model uses GPT-3 to perform RAG at lower cost and then summarizes the results to the user
    - this does result in increased latency per request, however the tradeoff makes the application much more finanically viable as a hobby project per request

# Learings and Highlights
- when project was release GPT-4 was the most advanced model available for conversation, however resulted in high cost for RAG and user reponses
- A bot swarm was used to reduce per query cost by 10x at cost of marginal increase in latency
    - A GPT 4 bot converses with the user and can call a GPT 3.5 bot as a tool when additional information is needed to answer query 
    - GPT 3.5 bot is performs RAG on corpus of game information when needed at fractional per token cost vs GPT 4
    - GPT 4 summarizes information and send message back to user to maintain high quality conversation ability
- Streamlit by default stateless, therefore all api objects should be stored in "st.session_state" if peristent conversation context is desired
