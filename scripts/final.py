"""
    Ejemplo 5 - Este programa comprueba el tipo de mensaje que se ha recibido
    Escrito por Transductor
    www.robologs.net
"""

# Importar librerias
import json
import requests

# Variables para el Token y la URL del chatbot
TOKEN = "1178941353:AAHPX0hYvHh0CmBC2v3Y-3khLpb3iKaBkTc"  # Cambialo por tu token
URL = "https://api.telegram.org/bot" + TOKEN + "/"


def update(offset):
    # Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))

    # Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")

    # Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)

    # Devolver este diccionario
    return mensajes_diccionario


def info_mensaje(mensaje):
    # Comprobar el tipo de mensaje
    if "text" in mensaje["message"]:
        tipo = "texto"
    elif "sticker" in mensaje["message"]:
        tipo = "sticker"
    elif "animation" in mensaje["message"]:
        tipo = "animacion"  # Nota: los GIF cuentan como animaciones
    elif "photo" in mensaje["message"]:
        tipo = "foto"
    else:
        # Para no hacer mas largo este ejemplo, el resto de tipos entran
        # en la categoria "otro"
        tipo = "otro"

    # Recoger la info del mensaje (remitente, id del chat e id del mensaje)
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]

    # Devolver toda la informacion
    return tipo, id_chat, persona, id_update


def leer_mensaje(mensaje):
    # Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensaje["message"]["text"]

    # Devolver las dos id, el nombre y el texto del mensaje
    return texto


def enviar_mensaje(idchat, texto):
    # Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))


# Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0

while (True):
    mensajes_diccionario = update(ultima_id)
    for i in mensajes_diccionario["result"]:

        # Guardar la informacion del mensaje
        tipo, idchat, nombre, id_update = info_mensaje(i)

        # Generar una respuesta dependiendo del tipo de mensaje
        if tipo == "texto":
            texto = leer_mensaje(i)
            texto_respuesta = "Has escrito: \"" + texto + "\""
        elif tipo == "sticker":
            texto_respuesta = "Bonito sticker!"
        elif tipo == "animacion":
            texto_respuesta = "Me gusta este GIF!"
        elif tipo == "foto":
            texto_respuesta = "Bonita foto!"
        elif tipo == "otro":
            texto_respuesta = "Es otro tipo de mensaje"

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        # Enviar la respuesta
        enviar_mensaje(idchat, texto_respuesta)

    # Vaciar el diccionario
    mensajes_diccionario = []