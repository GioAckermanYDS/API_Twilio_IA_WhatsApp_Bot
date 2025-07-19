# Twilio-OpenAI-WhatsApp-Bot/app/openai_utils.py

import os 
import json
from dotenv import load_dotenv
from litellm import completion
from app.prompts import SUMMARY_PROMPT

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["LITELLM_PROVIDER"] = "openai"

DEFAULT_LLM_MODEL = os.getenv("LLM_MODEL", "openrouter/google/gemini-2.5-pro")
print(f"🔍 Modelo actual cargado desde .env: {DEFAULT_LLM_MODEL}")


# Deducción automática del proveedor
vendor_name = DEFAULT_LLM_MODEL.split("/")[0]  # "openrouter", "groq", "bedrock", etc.
model_vendor = {
    DEFAULT_LLM_MODEL: vendor_name
}
os.environ["LITELLM_MODEL_VENDOR_JSON"] = json.dumps(model_vendor)


# IF YOU WANT TO ADD MORE MODELS
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# REGION_NAME = os.getenv("REGION_NAME")

# os.environ['GROQ_API_KEY'] = GROQ_API_KEY
# os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
# os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
# os.environ["AWS_REGION_NAME"] = REGION_NAME

# Constants
TEMPERATURE = 0.1
MAX_TOKENS = 350
STOP_SEQUENCES = ["==="]
TOP_P = 1
TOP_K = 1
BEST_OF = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0


SUPPORTED_MODELS = {
        # openrouter gratuitos
    "openrouter/mistralai/mistral-small-24b-instruct-2501:free",
    "openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
     "openrouter/google/gemini-2.5-pro",
    # openrouter Llama models
    "openrouter/anthropic/claude-3-opus",
    "openrouter/meta-llama/llama-3-70b-instruct",
    "openrouter/mistralai/mixtral-8x7b",
    "openrouter/openai/gpt-4o",
    # Groq Llama models
    "groq/llama3-8b-8192", 
    "groq/llama-3.1-8b-instant", 
    "groq/llama-3.1-70b-versatile", 
    # OpenAI models
    "gpt-3.5-turbo-0125",
    "gpt-4o", 
    "gpt-4o-mini",
    "gpt-4-0125-preview",
    # Amazon Anthropic models
    "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
    "bedrock/anthropic.claude-3-opus-20240229-v1:0",
    "bedrock/anthropic.claude-v2:1",
    }


def gpt_without_functions(model, stream=False, messages=[]):
    """ GPT model without function call. """
    if model not in SUPPORTED_MODELS:
        return False
    response = completion(
        model=model, 
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
        stream=stream
    )
    return response 



def summarise_conversation(history):
    """Summarise conversation history in one sentence"""

    conversation = ""
    for item in history[-70:]:
        if 'user_input' in item:
            conversation += f"User: {item['user_input']}"
        if 'bot_response' in item:
            conversation += f"Bot: {item['bot_response']}"

    openai_response = gpt_without_functions(
        model=DEFAULT_LLM_MODEL,
        stream=False,
        messages=[
            {'role': 'system', 'content': SUMMARY_PROMPT}, 
            {'role': 'user', 'content': conversation}
        ])

    chatbot_response = openai_response.choices[0].message.content.strip()

    return chatbot_response
