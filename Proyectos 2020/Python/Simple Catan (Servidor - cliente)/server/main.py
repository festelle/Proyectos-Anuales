from servidor import Server
import json

#Se abre el archivo de parámetros y guarda como un dict
with open('parametros.json',) as file:
    json_deserializado = json.load(file)


host = json_deserializado["host"]
port = json_deserializado["port"]



if __name__ == "__main__":

    server = Server(port, host)