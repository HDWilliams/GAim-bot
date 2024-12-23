#FUNCTION TO CREATE CHAT INTERFACE
import streamlit as st
from assistant_interface import  add_message_to_thread, get_assitant_messages

def create_chat_interface(client, conversation_thread, conversation_assistant, get_research):
  """
  client: streamlit client object
  conversation_thread: gpt conversation thread
  conversation_assistant: gpt conversation assistant object
  get_research: function from Research object to allow gpt research model to get info for conversational model

  returns None
  
  """
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
          user_message = add_message_to_thread(st.session_state.conversation_thread, prompt, st.session_state.client)
          message = get_assitant_messages(st.session_state.client, st.session_state.conversation_thread, st.session_state.conversation_assistant, function=get_research)

          st.session_state.messages.append({"role": "assistant", "content": message})
          st.chat_message("assistant").write(message)
      st.session_state["disable_chat_input"] = False