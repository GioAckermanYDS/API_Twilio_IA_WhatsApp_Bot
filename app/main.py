import os
import json
from datetime import datetime
from dotenv import load_dotenv

from fastapi import Form, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from twilio.rest import Client

from app.cookies_utils import set_cookies, get_cookies, clear_cookies
from app.prompts import SYSTEM_PROMPT
from app.openai_utils import gpt_without_functions, summarise_conversation
from app.redis_utils import redis_conn
from app.logger_utils import logger

# Cargar variables de entorno desde un archivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

app = FastAPI(
    title="Twilio-OpenAI-WhatsApp-Bot",
    description="Twilio OpenAI WhatsApp Bot",
    version="0.0.1",
    contact={
        "name": "Lena Shakurova",
        "url": "http://shakurova.io/",
        "email": "lena@shakurova.io",
    }
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

def respond(to_number, message) -> None:
    """Send a message via Twilio WhatsApp"""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER]):
        raise ValueError("Faltan credenciales de Twilio.")

    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.messages.create(
        body=message,
        from_="whatsapp:" + TWILIO_WHATSAPP_NUMBER,
        to="whatsapp:" + to_number.replace("whatsapp:", "").replace("+", "")
    )



@app.post('/whatsapp-endpoint')
async def whatsapp_endpoint(request: Request, From: str = Form(...), Body: str = Form(...)):
    logger.info(f'WhatsApp endpoint triggered...')
    logger.info(f'Request: {request}')
    logger.info(f'Body: {Body}')
    logger.info(f'From: {From}')

    query = Body
    phone_no = From.replace('whatsapp:+', '')
    chat_session_id = phone_no

    # Recuperar el historial de chat de Redis
    history = get_cookies(redis_conn, f'whatsapp_twilio_demo_{chat_session_id}_history') or []
    if history:
        history = json.loads(history)
    
    # Añadir la consulta del usuario al historial de chat
    history.append({"role": 'user', "content": query})

    # Resumir el historial de conversaciones
    history_summary = summarise_conversation(history)

   # Formatee el mensaje del sistema con el resumen de la conversación y la fecha actual
    system_prompt = SYSTEM_PROMPT.format(
            history_summary=history_summary,
            today=datetime.now().date()
    )

    # Obtenga una respuesta del modelo GPT de OpenAI
    openai_response = gpt_without_functions(
                        model="gpt-4o",
                        stream=False,
                        messages=[
                            {'role': 'system', 'content': system_prompt}, 
                            {'role': 'assistant', 'content': "Hi there, how can I help you?"}
                        ] + history)
    chatbot_response = openai_response.choices[0].message.content.strip()

    # Anexar la respuesta del asistente al historial de chat en Redis
    history.append({'role': 'assistant', 'content': chatbot_response},)
    set_cookies(redis_conn, name=f'whatsapp_twilio_demo_{chat_session_id}_history', value=json.dumps(history))

   # Envía la respuesta del asistente al usuario vía WhatsApp
    respond(From, chatbot_response)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host='0.0.0.0', port=3002, reload=True)