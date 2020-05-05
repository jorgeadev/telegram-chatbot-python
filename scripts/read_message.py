"""
    Ejemplo 1 - Este programa escribe por consola el contenido del último mensaje que ha recibido el chatbot junto con
    el nombre del autor y la ID del chat.

    @author Jorge Alberto Gomez Gomez
    @date may 01 of 2020
"""

# Import libraries
import json
import requests

# Variables para el token y la URL del chatbot
TOKEN = "1178941353:AAHPX0hYvHh0CmBC2v3Y-3khLpb3iKaBkTc"
URL = "https://api.telegram.org/bot" + TOKEN + "/"


def update():
    # LLamar al método getUpdates del bot haciendo una petición HTTPS (se obtiene una respuesta codificada)
    respuesta = requests.get(URL + "getUpdates")

    # Decodificar la respuesta recibida a formato UTF8 (se obtiene un string JSON)
    mensaje_js = respuesta.content.decode("utf8")

    # Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensaje_js)

    # Devolver este diccionario
    return mensajes_diccionario


def read_messaje():
    # Call update() and save the dictionary with recent messages
    get_messages = update()

    # Calculate the index of the last received message
    index = len(get_messages["result"]) - 1

    # Extract text, name of person and id of the last received message
    text = get_messages["result"][index]["message"]["text"]
    person = get_messages["result"][index]["message"]["from"]["first_name"]
    id_chat = get_messages["result"][index]["message"]["chat"]["id"]

    # Show this information in windows
    print(person + " (id: " + str(id_chat) + ") ha escrito: " + text)


# Call function "read_message()"
read_messaje()