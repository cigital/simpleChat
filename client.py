import socket as socket
import threading

from pickle import loads, dumps
from datetime import datetime
from os import system, path, makedirs

import argparse
from readline import parse_and_bind
parse_and_bind("set editing-mode emacs") # Habilitar el historial de entrada

class ClienteSocket:
    def __init__(self, host, port):
        self.host , self.port = host, port
        self.conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_sock.connect((self.host, self.port))

        self.mantener_connexion = True
        # Configurar un hilo para manejar la recepción de datos del servidor
        self.recepcion_hilo = threading.Thread(target=self.recibir_datos, args=(self.conn_sock,))
        # Configurar un hilo para manejar la entrada del usuario
        self.entrada_hilo = threading.Thread(target=self.enviar_datos, args=(self.conn_sock,))

        self.client_ip = socket.gethostbyname(socket.gethostname())
        self.client_port = self.conn_sock.getsockname()[1]
        self.client_ip_port = f"{self.client_ip}:{self.client_port}"

        self.recepcion_hilo.start()
        self.entrada_hilo.start()

        self.HELP_STRING = """Commands:
             help: Muestra este texto de ayuda.
             cls: Limpia la pantalla de la terminal.     
             chat.exit: Permite salir del chat."""
    

    def recibir_datos(self, socket_client):
        print("Esperando datos...")
        while self.mantener_connexion:
            try:
                datos_recibidos = socket_client.recv(1024)
                if not datos_recibidos:
                    print("\nServer closed, closing client, press [ENTER] if still open.")
                    break
    
                unserialized_data = loads(datos_recibidos)
                print(f"\n╭──[ {unserialized_data[0]} ] ── [ {self.print_colored(unserialized_data[1], 'azul')} ] {self.print_colored('➜', 'amarillo')} {unserialized_data[2]}")
                print(f"\r╰──[{self.print_colored('✔', 'verde')}] ➜ ", end="")
            except ConnectionAbortedError:
                print("[ConnectionAbortedError] Conexión cerrada por el servidor.")
                break
            except BrokenPipeError:
                print("[BrokenPipeError] Cerrando el programa.")
                break 
            except Exception as e:
                print(f"[UnexpectedError] {e}")
                break
        self.mantener_connexion = False

    def enviar_datos(self, socket_client):
        while self.mantener_connexion:
            try:
                hora = datetime.now().strftime("(%Y/%m/%d) %H:%M:%S")
                mensaje = str(input(""))
                match mensaje:
                    case mensaje if mensaje.casefold() == "chat.exit":
                        break
                    case mensaje if not mensaje: # Si el mensaje esta vacio se ignora y no se envia, se sigue el bucle
                        continue
                    case mensaje if mensaje == "cls":
                        system('clear || cls')
                        print(f"╰──[{self.print_colored('✔', 'verde')}] ➜ ", end="")
                        continue
                    case mensaje if mensaje.casefold() == "help":
                        print(self.HELP_STRING)
                        print(f"╰──[{self.print_colored('✔', 'verde')}] ➜ ", end="")
                        continue
            except KeyboardInterrupt:
                print("\nCerrando conexión y saliendo del programa por KeyboardInterrupt error.")
                break
            else:
                to_send = (hora, self.client_ip_port, mensaje)
                serialized_data = dumps(to_send)
                socket_client.send(serialized_data)
        self.exit_connection()
    
    @staticmethod
    def print_colored(caracter, color):
        colores = {
            'rojo': '\033[91m',
            'verde': '\033[92m',
            'amarillo': '\033[93m',
            'azul': '\033[94m',
            'reset': '\033[0m'
        }

        # Verificar si el color es válido
        if color not in colores.keys():
            print(f"Invalid color '{color}'")
            return

        # Devolver  carácter con el color especificado
        return f"{colores[color]}{caracter}{colores['reset']}"

    def exit_connection(self):
        try:
            print("\nExiting...", end="")
            self.mantener_connexion = False
            self.conn_sock.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"EXIT CONNECTION ERROR\n{e}")
        else:
            print("exited.")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Servidor TCP")
        parser.add_argument("--ip", help="Dirección IPv4 (recomendado: 127.0.0.1)")
        parser.add_argument("--port", help="Puerto, tiene que ser un puerto disponible o salta error.", type=int)
        args = parser.parse_args()

        ipv4_address = args.ip
        port = args.port

        if ipv4_address is None:
            ipv4_address = str(input("IPv4 address: "))
        if port is None:
            port = int(input("Port: "))

    except KeyboardInterrupt:
        print("\nbye.")
    except ValueError as ve:
        print(f"Error {ve}")
        print("""Informacación incorrecta, asegurate que tener un formato correcto o prueba con otro puerto. Ej:
                IPv4 address: 127.0.0.1
                Port: 12345""")
    else:
        try:
            cliente = ClienteSocket(ipv4_address, port)
        except Exception as e:
            print(f"Error {e}")
            print("""Error al crear el objeto de cliente, tal vez no ingresaste correctamente los datos. Ejemplo:
                     Dirección IPv4: 127.0.0.1
                     Puerto: 12345
                
                 O prueba con otro puerto.
                 Intentar otra vez.
                """)
