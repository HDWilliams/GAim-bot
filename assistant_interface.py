import os
from openai import OpenAI 
import streamlit as st
import logging

def create_assistant(client: OpenAI, setup_prompt, model="gpt-4o"):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id=st.secrets["ASSISTANT_ID"])
        return assistant
    except Exception as e:
        logging.error(f"Error creating assistant: {e}")
        st.error(f"Sorry it seems there was an error: {e}")
        return None

def create_vector_store(client, files):
    try:
        vector_store = client.beta.vector_stores.create(name="Eldin Ring Info")
        file_paths = files
        file_streams = [open(path, "rb") for path in file_paths]

        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        logging.info(f"File batch status: {file_batch.status}")
        logging.info(f"File counts: {file_batch.file_counts}")
        return vector_store
    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        st.error(f"Sorry it seems there was an error: {e}")
        return None

def attach_vector_store(client, assistant, vector_store_id):
    try:
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        return assistant
    except Exception as e:
        logging.error(f"Error attaching vector store: {e}")
        st.error(f"Sorry it seems there was an error: {e}")
        return None

def create_assistant_and_store(client, setup_prompt, vector_store_id=None):
  assistant = create_assistant(client, setup_prompt)
  if vector_store_id is None:
    vector_store = create_vector_store(client)
    vector_store_id = vector_store.id
  assistant = attach_vector_store(client, assistant, vector_store_id)
  return assistant

def create_thread(client):
  try:
    thread = client.beta.threads.create()
    return thread
  except Exception as e:
    logging.error(f"Error attaching vector store: {e}")
    st.error(f"Sorry it seems there was an error: {e}. Please reload the page")
    return None


def add_message_to_thread(thread, content, client):
  try:
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=content
    )
    return message
  except Exception as e:
    logging.error(f"Error attaching vector store: {e}")
    st.error(f"Sorry it seems there was an error: {e}")
    return None


def get_assitant_messages(client, thread, assistant):
  try:
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id, assistant_id=assistant.id, 
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")
    #print(message_content.value)
    #print("\n".join(citations))
    return message_content.value
  except Exception as e:
    logging.error(f"Error attaching vector store: {e}")
    st.error(f"Sorry it seems there was an error: {e}")
    return None