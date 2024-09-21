from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from dotenv import load_dotenv
import os
from groq import Groq
from fastapi.responses import PlainTextResponse


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API key desde la variable de entorno
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API key en las variables de entorno")

# Inicializa el cliente de Groq con la API key obtenida
client = Groq(api_key=api_key)

# Inicializa FastAPI
app = FastAPI()

# Diccionario para almacenar el historial de conversación por usuario
conversation_history = {}

# Ruta para recibir los mensajes de WhatsApp
@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    # Obtén el contenido del mensaje entrante
    form_data = await request.form()
    incoming_msg = form_data.get('Body')
    # Obtenemos el número de teléfono del usuario
    # Si no se proporciona el campo 'From', usar un valor predeterminado para las pruebas
    user_number = form_data.get('From', 'test-user')  # Simulamos un número para las pruebas

    # Si el usuario no tiene historial, inicializamos su historial
    if user_number not in conversation_history:
        conversation_history[user_number] = [
            {"role": "system", "content": "Eres un asistente amigable, te debes expresar con emojis y siempre debes dar respuestas sencillas, cortas y en español."}
        ]

    # Agregamos el nuevo mensaje del usuario al historial
    conversation_history[user_number].append({"role": "user", "content": incoming_msg})

    print(f"Mensaje recibido: {incoming_msg}")
    print(f"Historial recibido: {conversation_history[user_number]}")
# Procesa el mensaje usando OpenAI (GPT)
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation_history[user_number]
        )
        reply = chat_completion.choices[0].message.content
        # Agregamos la respuesta del asistente al historial
        conversation_history[user_number].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"Lo siento, hubo un error: {str(e)}"

    # Responder usando Twilio
    #resp = MessagingResponse()
    #resp.message(reply)
    return PlainTextResponse(str(reply))
