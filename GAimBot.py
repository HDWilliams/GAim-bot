import os
import streamlit as st
from openai import OpenAI
from assistant_interface import  create_thread, create_assistant, add_message_to_thread, get_assitant_messages, attach_vector_store, retrieve_assistant
from retrieval_tool import ResearchTool


#CREATE CLIENT OBJECT
api_key = st.secrets["OPENAI_SECRET_KEY"]
client = OpenAI(api_key=api_key)

#CREATE ASSISTANTS AND THREADS
conversation_assistant = create_assistant(client, st.secrets["CONVERSATION_ASSISTANT_INSTRUCTIONS"], model="gpt-4o", tools=[
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
    
])

conversation_thread = create_thread(client)  

research_assistant = create_assistant(client, st.secrets["RESEARCH_ASSISTANT_INSTRUCTIONS"], model="gpt-3.5-turbo", tools=[{"type":"file_search"}])
research_thread = create_thread(client)
research_assistant = attach_vector_store(client, research_assistant, st.secrets["VECTOR_STORE"])

#CREATE FUNCTION TO CALL RESEARCH GPT ASSISTANT
get_research = ResearchTool(client,research_assistant, research_thread).retrieve_info

#CHAT INTERFACE
st.title("GAim Bot")
if "disable_chat_input" not in st.session_state:
    st.session_state["disable_chat_input"] = False

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": st.secrets["CONVERSATION_STARTER"]}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(max_chars=250, disabled=st.session_state["disable_chat_input"]):
    #DISABLE USER INPUT WHILE WAITING FOR MESSAGE
    if not st.session_state["disable_chat_input"]:

        #ADD USER MESSAGE TO MESSAGE LIST
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        #GET GPT RESPONSE AND 
        user_message = add_message_to_thread(conversation_thread, prompt, client)
        message = get_assitant_messages(client, conversation_thread, conversation_assistant, function=get_research)

        st.session_state.messages.append({"role": "assistant", "content": message})
        st.chat_message("assistant").write(message)
    st.session_state["disable_chat_input"] = False

