import json
import requests
from utils.config import OPENAI_API_KEY, AI_MODEL
from tenacity import retry, wait_random_exponential, stop_after_attempt

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def send_api_request_to_openai_api(messages, functions=None, function_call=None, model=AI_MODEL, openai_api_key=OPENAI_API_KEY):
    """Send the API request to the OpenAI API via Chat Completions endpoint."""
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}
        json_data = {"model": model, "messages": messages}
        if functions:
            json_data.update({"functions": functions})
        if function_call:
            json_data.update({"function_call": function_call})
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to OpenAI API due to: {e}")

def execute_function_call(function_name, arguments, api_key=OPENAI_API_KEY):
    """Execute a function call based on provided function name and arguments."""
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        json_data = {
            "function_name": function_name,
            "arguments": arguments
        }
        response = requests.post("https://api.example.com/execute", headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()  # Assuming the response is in JSON format
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to execute function call due to: {e}")
