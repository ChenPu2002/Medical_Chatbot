import os
import glob
from openai import OpenAI
from dotenv import load_dotenv
import time
from openai import AssistantEventHandler

load_dotenv('.env')
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def create_vector_store(name, file_paths):
    try:
        vector_store = client.beta.vector_stores.create(name=name)
        file_streams = [open(path, "rb") for path in file_paths]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file_streams)
        print("Files uploaded successfully.")
        for stream in file_streams:
            stream.close()
        return vector_store.id
    except Exception as e:
        for stream in file_streams:
            stream.close()
        print(f"Failed to upload files: {e}")
        raise

def setup_assistant(vector_store_id):
    try:
        assistant = client.beta.assistants.create(
            name="Medical Assistant with File Search",
            instructions="You are a clinical doctor, skilled in diagnosing diseases from descriptions of symptoms. Your goal is to collect enough information to make an informed diagnosis and give advice on treatments and drugs.",
            model="gpt-4-turbo",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        )
        return assistant.id
    except Exception as e:
        print(f"Failed to create assistant: {e}")
        raise



class EventHandler(AssistantEventHandler):
    def __init__(self):
        self.complete_response = []

    def on_text_delta(self, delta, snapshot):
        # Append text as it comes in
        print(delta.value, end="", flush=True)
        self.complete_response.append(delta.value)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)
      
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
                    

def get_response(assistant_id, user_input, conversation_history, prompt_text, thread_id=None):
    try:
        if thread_id is None:
            # Create a new thread if no thread_id is passed
            thread = client.beta.threads.create(messages=conversation_history)
            thread_id = thread.id
        else:
            # Add the new user message to the existing thread
            message = {"role": "user", "content": user_input}
            client.beta.threads.messages.create(thread_id=thread_id, message=message)

        # Create an instance of the event handler
        event_handler = EventHandler()

        # Start streaming the response
        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=prompt_text,
            event_handler=event_handler
        ) as stream:
            stream.until_done()

        # The final complete response is collected in event_handler.complete_response
        response_content = "".join(event_handler.complete_response)
        
        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

        return response_content, conversation_history, thread_id
    except Exception as e:
        print(f"Failed to get response: {e}")
        raise

