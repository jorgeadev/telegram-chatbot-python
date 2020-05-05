"""
    Ejemplo 2 - Este programa genera una respuesta si se recibe un mensaje con las palabras "Hola" o "Adiós"

    @author Jorge Alberto Gomez Gomez
    @date may 01 of 2020
"""

# Import libraries
import json
import requests
import time

# Variables para el token y la URL del chatbot
TOKEN = "1178941353:AAHPX0hYvHh0CmBC2v3Y-3khLpb3iKaBkTc"
URL = "https://api.telegram.org/bot" + TOKEN + "/"


def update():
    # Call method getUpdates of the bot
    response = requests.get(URL + "getUpdates")

    # Decode received response to format UTF8
    messaje_js = response.content.decode("utf8")

    # Convert the string JSON to a Python dictionary
    messaje_dictionary = json.loads(messaje_js)

    # Return dictionary
    return messaje_dictionary


def read_messaje():
    # Save dictionary with all recent messages
    get_messages = update()

    # Calculate the index of the last received message
    index = len(get_messages["result"]) - 1

    # Extract text, name of person and id of the last received message
    text = get_messages["result"][index]["message"]["text"]
    person = get_messages["result"][index]["message"]["from"]["first_name"]
    id_chat = get_messages["result"][index]["message"]["chat"]["id"]

    # Return the id, name and text of the message
    return id_chat, person, text


def send_message(id_chat, text):
    # Call method sendMessage of the bot passing the text an chat id
    requests.get(URL + "sendMessage?text=" + text + "&chat_id=" + str(id_chat))


# Call functions "read_message"
id_chat, name, text = read_messaje()

greeting_list = ["Hola", "hola", "Hello", "hello", "Hi", "hi"]
farewell_list = ["Bye", "bye", "adios", "Adios", "adiós", "Adiós", "Hasta luego", "hasta luego", "Hasta pronto", "hasta pronto"]

count = 0
while True:
    time.sleep(5)
    if count % 20 == 0:
        print("Is the answer number: " + str(count) + " that we receive from the server ...")
    # Generate a response from the message information
    for i in greeting_list:
        if i in text:
            response_text = "Hello, " + name + "!"
            send_message(id_chat, response_text)

    for i in farewell_list:
        if i in text:
            response_text = "See you soon!"
            send_message(id_chat, response_text)
    count += 1