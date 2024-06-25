import os
import streamlit as st
from openai import OpenAI
from assistant_interface import create_assistant_and_store, create_thread, add_message_to_thread, get_assitant_messages 
from assistant_instructions import setup_prompt

api_key = st.secrets["OPENAI_SECRET_KEY"]

client = OpenAI(api_key=api_key)


assistant = create_assistant_and_store(client, setup_prompt, st.secrets["VECTOR_STORE"])
thread = create_thread(client)  

st.title("Your Curly Companion")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! What questions do you have about culry, afro and textured hair. I can answer questions, give tips, design a haircare routine and more..."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    user_message = add_message_to_thread(thread, prompt, client)

    message = get_assitant_messages(client, thread, assistant)


    st.session_state.messages.append({"role": "assistant", "content": message})
    st.chat_message("assistant").write(message)

