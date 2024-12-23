from assistant_interface import add_message_to_thread, get_assitant_messages

class ResearchTool:
  def __init__(self, client, assistant, thread) -> None:
    self.client = client
    self.assistant = assistant
    self.thread = thread

  def retrieve_info(self, query):
    """pass user query to research assistant, to retrieve data from vector store. return data as str, data organized in bullet point format
      args:
        client (object): openai sdk client instance
        query (str): summarized user query for look up 
    """
    add_message_to_thread(self.thread, content=query, client=self.client)
    return get_assitant_messages(self.client, self.thread, self.assistant)