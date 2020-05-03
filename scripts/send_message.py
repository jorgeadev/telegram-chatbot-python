"""
    Ejemplo 3 - Este tercer programa utiliza un offset para controlar los mensajes que se han contestado y los que no.

    @author Jorge Alberto Gomez Gomez
    @date may 02 of 2020
"""

# Import libraries
import json
import requests

# Variables para el token y la URL del chatbot
TOKEN = "1178941353:AAHPX0hYvHh0CmBC2v3Y-3khLpb3iKaBkTc"
URL = "https://api.telegram.org/bot" + TOKEN + "/"


def update(offset):
    # Call method getUpdates of the bot
    response = requests.get(URL + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))
    # Telegram will return all messages with id equal o higher to offset

    # Decode received response to format UTF8
    messaje_js = response.content.decode("utf8")

    # Convert the string JSON to a Python dictionary
    messaje_dictionary = json.loads(messaje_js)

    # Return dictionary
    return messaje_dictionary


def read_messaje(get_messages):
    # Extract text, name of person and id of the last received message
    text = get_messages["message"]["text"]
    person = get_messages["message"]["from"]["first_name"]
    id_chat = get_messages["message"]["chat"]["id"]

    # Calcular el identificador único del mensaje para calcular el offset
    id_update = get_messages["update_id"]

    # Return the id, name and text of the message
    return id_chat, person, text, id_update


def send_message(id_chat, text):
    # Call method sendMessage of the bot passing the text an chat id
    requests.get(URL + "sendMessage?text=" + text + "&chat_id=" + str(id_chat))


# Variable para almacenar la ID del último mensaje procesado
last_id = 0

greeting_list = ["Hola", "hola", "Hello", "hello", "Hi", "hi"]
farewell_list = ["Bye", "bye", "adios", "Adios", "adiós", "Adiós", "Hasta luego", "hasta luego", "Hasta pronto", "hasta pronto"]

while True:
    message_dictionary = update(last_id)
    for i in message_dictionary["result"]:

        # LLamar a la función "read_message"
        id_chat, name, text, id_update = read_messaje(i)

        # Si la ID del mensaje es mayor que el último, se guarda la ID + 1
        if id_update > (last_id - 1):
            last_id = id_update + 1

        # Generate a response from the message information
        if "Hola" in text:
            response_text = "Hello, " + name + "!"
        elif "Adios" in text:
            response_text = "See you soon!"
        else:
            response_text = "Has escrito: \"" + text + "\""
        send_message(id_chat, response_text)
    message_dictionary = []