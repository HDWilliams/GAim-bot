import os
from openai import OpenAI 
import streamlit as st
import logging

def create_assistant(client: OpenAI, instructions, model="gpt-4o", tools=None):
    try:
        assistant = client.beta.assistants.create(model=model, instructions=instructions, tools=tools)
        return assistant
    except Exception as e:
        logging.error(f"Error creating assistant: {e}")
        st.error(f"Sorry it seems there was an error: {e}")
        return None
    
def retrieve_assistant(client: OpenAI, assistant_retrieval_id=None):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_retrieval_id)
        return assistant
    except Exception as e:
        logging.error(f"Error retrieving assistant: {e}")
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

def create_thread(client):
  try:
    thread = client.beta.threads.create()
    return thread
  except Exception as e:
    logging.error(f"Error creating thread: {e}")
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
    logging.error(f"Error adding message to thread: {e}")
    st.error(f"Sorry it seems there was an error: {e}")
    return None

def get_assitant_messages(client, thread, assistant, function=None):
  try:
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id, assistant_id=assistant.id, 
    )
    if run.status == "requires_action":
      print(run.status)

      prev_user_message_content = client.beta.threads.messages.list(thread_id=thread.id).data[-1].content[0].text.value
      print(prev_user_message_content)

      tool_outputs = []
      for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_research":
          tool_outputs.append({
            "tool_call_id": tool.id,
            "output": function(prev_user_message_content)
          })
          print(tool_outputs)
      
      if tool_outputs:
        try:
          run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
          )
          print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
        else:
          print("No tool outputs to submit.")
    elif run.status == "failed":
        print("failed")
        raise Exception
          
    if run.status == "completed":
      print("Run completed")
      messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
      message_content = messages[0].content[0].text
      annotations = message_content.annotations
      citations = []
      for index, annotation in enumerate(annotations):
          message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
          if file_citation := getattr(annotation, "file_citation", None):
              cited_file = client.files.retrieve(file_citation.file_id)
              citations.append(f"[{index}] {cited_file.filename}")
    
      return message_content.value
      
    
  except Exception as e:
    print(e)
    logging.error(f"Error sending messages: {e}")
    st.error(f"Sorry it seems there was an error: {e}")
    return None