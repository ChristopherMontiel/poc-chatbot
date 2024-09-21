from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from dotenv import load_dotenv
import os
from groq import Groq
from fastapi.responses import PlainTextResponse


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializa FastAPI
app = FastAPI()

# URL base para el LLM local
client = Groq(
    api_key="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"
)

# Ruta para recibir los mensajes de WhatsApp
@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    # Obtén el contenido del mensaje entrante
    form_data = await request.form()
    incoming_msg = form_data.get('Body')
# Procesa el mensaje usando OpenAI (GPT)
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable, te debes expresar con emojis y siempre debes dar respuestas sencillas, cortas y en español."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        reply = f"Lo siento, hubo un error: {str(e)}"

    # Responder usando Twilio
    resp = MessagingResponse()
    #resp.message(reply)
    resp.message("Respuesta generica de prueba")
    return PlainTextResponse(str(resp))
