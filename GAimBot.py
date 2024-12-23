import os
import streamlit as st
from openai import OpenAI
from assistant_interface import  create_thread, create_assistant, add_message_to_thread, get_assitant_messages, attach_vector_store, retrieve_assistant
from ResearchTool import ResearchTool
from gpt_tools import tools
from chat_interface import create_chat_interface

#TO HAVE PERSISTENT SESSION MEMORY ALL OPENAI API OBJECTS MUST BE STORED IN SESSION 

#CREATE CLIENT OBJECT
api_key = st.secrets["OPENAI_SECRET_KEY"]

if 'client' not in st.session_state:
    client = OpenAI(api_key=api_key)
    st.session_state.client = client

#CREATE ASSISTANTS AND THREADS
if 'conversation_assistant' not in st.session_state:
    conversation_assistant = create_assistant(
        client, 
        st.secrets["CONVERSATION_ASSISTANT_INSTRUCTIONS"], 
        model=st.secrets["GPT_MODEL"], 
        tools=tools)
    st.session_state.conversation_assistant = conversation_assistant

if 'conversation_thread' not in st.session_state:
    conversation_thread = create_thread(client)
    st.session_state.conversation_thread = conversation_thread  

if "research_assistant" not in st.session_state:
    research_assistant = create_assistant(st.session_state.client, st.secrets["RESEARCH_ASSISTANT_INSTRUCTIONS"], model=st.secrets["GPT_MODEL_RESEARCH"], tools=[{"type":"file_search"}])
    st.session_state.research_assistant = research_assistant

if "research_thread" not in st.session_state:
    research_thread = create_thread(st.session_state.client)
    st.session_state.research_thread = research_thread

st.session_state.research_assistant = attach_vector_store(st.session_state.client, st.session_state.research_assistant, st.secrets["VECTOR_STORE"])

#CREATE FUNCTION TO CALL RESEARCH GPT ASSISTANT
get_research = ResearchTool(st.session_state.client ,st.session_state.research_assistant, st.session_state.research_thread).retrieve_info

#CHAT INTERFACE TO DISPLAY MESSAGES TO USER
st.title("GAim Bot")
create_chat_interface(
    st.session_state.client, 
    st.session_state.conversation_thread, 
    st.session_state.conversation_assistant, 
    get_research)
  

