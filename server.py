import socket
import socketserver
import threading
import sqlite3

from pickle import loads, dumps
from datetime import datetime

from os import system
from time import sleep

import argparse
from readline import parse_and_bind
parse_and_bind("set editing-mode emacs") # Habilitar el historial de entrada

# Clase que maneja las solicitudes de los clientes
class ServidorChat(socketserver.BaseRequestHandler):
    """
        Clase que implementa un servidor de chat con funcionalidad de control de comandos.

        Esta clase se encarga de manejar las conexiones de los clientes, recibir y enviar mensajes, y proporciona comandos de control
        para administrar el servidor. Los mensajes de chat se almacenan en una base de datos SQLite.

        Args:
            request (socket): El socket de la solicitud de cliente.
            client_address (tuple): Una tupla que contiene la dirección IP y el puerto del cliente.
            server (socketserver.BaseServer): El servidor que maneja las conexiones.

        Attributes:
            date_and_time (str): Una cadena que representa la fecha y hora actual en el formato "%Y_%m_%d-%H_%M_ 
            mantener_connexion (bool): Una bandera que controla si el servidor debe mantener las conexiones activas.
            client_dict (dict): Un diccionario que mapea las direcciones IP y puertos de los clientes a sus sockets de conexión.
            mensajes (list): Una lista que almacena los mensajes de chat recibidos.
        
        Methods:
            __init__(self, request, client_address, server): Constructor de la clase.
            command_control_main(self): Función que maneja los comandos de control del servidor.
            setup(self): Inicializa una nueva conexión de cliente y registra al cliente.
            handle(self): Maneja la recepción de mensajes de los clientes.
            broadcast(self, data): Reenvía un mensaje a todos los clientes conectados.
            finish(self, target=()): Realiza tareas de limpieza al finalizar una conexión.
            remove_client(self, target_address: tuple): Elimina un cliente del servidor.
            log_this(self, text): Registra información en un archivo de registro.
            get_msg_db(self): Recupera mensajes de chat de la base de datos SQLite.
            save_into_db(self, data): Almacena un mensaje en la base de datos SQLite.
            clear_db(self): Borra todos los mensajes de la base de datos.
            send_msgs(self, target): Envía mensajes a un cliente recién conectado.
    """
    
    date_and_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    mantener_connexion = True
    client_dict = {}
    mensajes = []
    
    def __init__(self, request, client_address, server):
        self.get_msg_db()
        self.command_control = threading.Thread(target=self.command_control_main)
        self.command_control.start()
    
        # Llama al __init__ de la clase base
        super().__init__(request, client_address, server)
    
    def command_control_main(self):
        """
            Función principal que maneja los comandos de control del servidor.

            Esta función permite al administrador del servidor ejecutar comandos de control para gestionar la operación del servidor de chat. Los comandos disponibles se explican a continuación. 

            - 'help': Muestra un mensaje de ayuda que describe los comandos disponibles.
            - 'print-clients': Muestra en pantalla la lista de clientes conectados.
            - 'eject-client': Permite expulsar a un cliente del servidor.
            - 'print-msg': Imprime en pantalla los mensajes guardados en el servidor.
            - 'clear-db': Borra todos los mensajes almacenados en la base de datos.
            - 'cls': Limpia la pantalla de la terminal.
            - 'shutdown-server': Apaga el servidor, desconectando a todos los clientes.
            - 'exit': Permite salir del modo de control de comandos y volver al funcionamiento normal del servidor.

            Args:
                self (ServidorChat): La instancia de la clase ServidorChat que llama a esta función.
        
            No devuelve valores
        """

        def help_cmd():
            """ Muestra un mensaje de ayuda con la descripción de los comandos disponibles. """

            HELP_STRING = """Commands:
             help: Muestra este texto de ayuda.
             print-msg: Imprime en pantalla los mensajes guardados.
             print-clients: Imprime en pantalla los clientes connectados.
             eject-client: Permite expulsar a un cliente del servidor.
             global-message <message>: Permite enviar un mensaje a todos los cliente conectados.
             
             clear-db: Borra todos los mensajes.
             cls: Limpia la pantalla de la terminal.
             
             shutdown-server: Apaga el servidor, si se ejecuta 2 veces, va a salir del comando de control.
             exit: Permite salir del comando de control, debe usar-se 
                    despues de shutdown-server en caso de haber multiples usuarios conectados.
            """

            print(HELP_STRING)

        def print_msg():
            """ Imprime en pantalla los mensajes guardados en el servidor. """
            print(f" ------- [ Mensajes ] ------")
            print(*(f"|> [ {time} ]-[ {ip} ]-[ {message} ]" for time, ip, message in self.mensajes), sep="\n")
            print(f" ------------ [ Hay {len(self.mensajes)} mensajes ] ------------")
        
        def print_clients():
            """ Muestra en pantalla la lista de clientes conectados al servidor. """
            print(f"____[Client addresses]____")
            print("| [ IP ]"," "*6,"[ Port ] |")
            print(*(f"| {ip}{' '*8}{port} |" for ip, port in self.client_dict.keys()), sep="\n")
            print(f" -- [ Hay {len(self.client_dict.keys())} clientes ] --")

        def eject_client():
            """ Permite expulsar a un cliente del servidor. """
            try:
                target = input("Target address and port, separated by coma (ex: 127.0.0.1,12345 ): ")
                ip, puerto = target.split(",") 
                target_tuple = (ip, int(puerto))
                
                if len(target_tuple)>2:
                    print("Target format is incorrect, try again")
                    return

                if target_tuple in self.client_dict.keys():
                    self.remove_client(target_tuple)
                else:
                    print(f"{target_tuple}, not in client dict.")

            except Exception as ejectError:
                self.log_this(f" | --> [ EJECT ERROR ] error while ejecting target '{target}' \n{ejectError}")

        def shutdown_this_server():
            """ Apaga el servidor, desconectando a todos los clientes. """
            try:
                self.mantener_connexion = False
                print(f"\nCerrando el servidor...", end="")

                for client_sock in list(self.client_dict.values()):
                    with client_sock as client_sock:
                        client_sock.shutdown(socket.SHUT_RDWR)
                    
                self.server.shutdown()
                self.server.server_close()
            except Exception as e:
                print(f"\n[ SHUTDOWN SERVER ERROR ] \n{e}")
                self.log_this(f" | --> [ SHUTDOWN SERVER ERROR ] \n{e}")
            else:
                print("Servidor cerrado.")

        def global_message(message: str):
            """
                Permite enviar un mensaje a todos los clientes conectados.
        
                Args:
                    message (str): El mensaje que se enviará a todos los clientes.
            """

            actual_time = str(datetime.now().strftime("(%Y/%m/%d) %H:%M:%S"))
            server_message = (actual_time,'Server', message)
            self.broadcast(server_message)

        dict_of_commands = {
            "help": help_cmd,
            "print-clients": print_clients,
            "eject-client": eject_client,
            "print-msg": print_msg,
            "clear-db": self.clear_db,
            "cls": lambda: system('cls||clear'),
            "shutdown-server": shutdown_this_server,
            }

        while self.mantener_connexion:
            try:            
                command = str(input("\nEscribe algo > "))
            except EOFError:
                print("\nHaz presionado Ctrl+D, saliendo")
                shutdown_this_server()
                break
            except KeyboardInterrupt: # El usuario presionó Ctrl+D para salir
                print("\nbye.")
                break

            match command:
                case command if not command:
                    # Si el mensaje esta vacio se ignora y no se envia, se sigue el bucle
                    continue
                case command if command.split()[0].casefold()=="global-message" and len(command.split())>=2:
                    # Separa el mensaje solo por el primer espacio en blanco y selecciona el mensaje
                    global_message(command.split(" ", 1)[1]) 
                case command if command.casefold() == "exit":
                    shutdown_this_server()
                    break
                case command if command not in dict_of_commands.keys():
                    print("Esa acción no esta disponible, escriba: help")
                    continue
                case _:
                    dict_of_commands[command]()
        
    def setup(self):
        """ Inicializa una nueva conexión de cliente y registra al cliente. No recibe argumentos ni devuelve valor. """
        self.log_this(f"[ NUEVA CONEXIÓN ] {self.client_address}")

        # Añadimos el cliente al diccionario
        self.client_dict[self.client_address] = self.request

        # Envia los mensajes de la lista
        self.send_msgs(self.request, self.mensajes)

    def handle(self):
        """ Maneja la recepción de mensajes de los clientes. No recibe argumentos ni devuelve valor."""
        while self.mantener_connexion:
            try:
                data = self.request.recv(1024)
                if not data:
                    break # Si la data está vacia, cerramos la conexión
                
                # Handle pickle deserialization errors
                try:
                    unserialized_data = loads(data)
                except Exception as pick_e:
                    self.log_this(f" | --> [ HANDLE ERROR PICKLE ] \n{pick_e}")

                # Almacenamos el mensaje en la lista i base de datos
                self.mensajes.append(unserialized_data)
                self.save_into_db(unserialized_data)

                # Reenviamos                
                self.broadcast(unserialized_data)

            except ConnectionResetError as reset_error:
                print(f"\n[ HANDLE ERROR ConnectionResetError ] \n{reset_error}")
                self.log_this(f" | --> [ HANDLE ERROR ] \n{reset_error}")
                break
            except Exception as handle_error:
                print(f"\n[ HANDLE ERROR ] \n{handle_error}")
                self.log_this(f" | --> [ HANDLE ERROR ] \n{handle_error}")
                break

    def broadcast(self, data: tuple):
        """
            Reenvía un mensaje a todos los clientes conectados, remitente incluido.
                Args:
                    data (tuple): La tupla que representa un mensaje de chat a reenviar a los clientes.
                No tiene valor de retorno.
        """

        for target_address, client in self.client_dict.items():
            try:
                serialized_data = dumps(data)
                client.send(serialized_data)
                self.log_this(f" | --> [ Sending ] '{data}' from {self.client_address} to {target_address}.")
            except Exception as brderror:
                self.log_this(f"| --> [ BROADCAST ERROR ] removing client now:  {brderror}")
                self.remove_client(self.target_address)
 
    def finish(self, target=()):
        """
            Realiza tareas de limpieza al finalizar cualquier conexión, desde cualquier lugar,ya sea 
            conexion fnalizada por el servidor o el cliente.
                Args:
                    target (tuple, opcional): La dirección IP y puerto del cliente a eliminar. Valor predeterminado es una tupla vacía ().
                No tiene valor de retorno.
        """
    
        if not target:
            if self.client_address in self.client_dict.keys():
                del self.client_dict[self.client_address]
        else:
            self.remove_client(target)

        self.log_this(f"[ CONEXIÓN CERRADA ] {self.client_address}.")
    
    def remove_client(self, target_address: tuple):
        """
            Elimina un cliente del servidor.
                Args:
                    target_address (tuple): La dirección IP y puerto del cliente a eliminar.
                No tiene valor de retorno.
        """

        try:
            self.client_dict[target_address].shutdown(socket.SHUT_RDWR)
            del self.client_dict[target_address]
        except KeyError as keyrr:
            self.log_this(f"| --> [ REMOVE ERROR KeyError not found ] {keyrr}")
        else:
            print(f"\n[ Client removed ] {target_address}")
            self.log_this(f"| --> [ Client removed ] {target_address}.")

    def log_this(self, text):
        """
            Registra información en un archivo de registro.
                Args:
                    text (str): El texto que se registrará en el archivo de registro.
                No tiene valor de retorno.
        """

        with open(f"server-{self.date_and_time}.log", "a") as file:
            file.write(f"\n{text}")

    def get_msg_db(self):
        """ Recupera mensajes de chat de la base de datos SQLite. No recibe argumentos ni devuelve valor. """

        # Establece la conexion
        with sqlite3.connect('mi_base_de_datos.db') as conexion:
            cursor = conexion.cursor()
            res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat';")
            existe_tabla = cursor.fetchone() # Devuelve (nombretabla, ) si existe o devuelve None
        
            # Si la tabla no existe la crea y si existe, comprueba si esta vacia y si no lo esta, almacena los mensajes
            if not existe_tabla:
                actual_time = str(datetime.now().strftime("(%Y/%m/%d) %H:%M:%S"))
                default_msg = (actual_time,'Server','Bienvenido a esta herramienta')

                cursor.execute("CREATE TABLE chat(hora, usuario, texto)")
                cursor.execute("INSERT INTO chat(hora, usuario, texto) VALUES (?,?,?)", default_msg)
                conexion.commit()

                self.log_this("> Tabla creada")
                self.mensajes = [cursor.execute("SELECT * FROM chat").fetchall()[0]]
            else: 
                self.log_this(f"> Existe la tabla {existe_tabla[0]}")

                # Contea el numero de mensajes
                cursor.execute("SELECT COUNT(*) FROM chat")
                count = cursor.fetchone()[0]
                
                self.log_this(f"> La tabla {existe_tabla[0]} tiene {count} mensajes.")

                if count != 0:
                    self.mensajes = cursor.execute("SELECT * FROM chat").fetchall()
    
    def save_into_db(self, data):
        """
            Almacena un mensaje en la base de datos SQLite.
            Args:
                data (tuple): La tupla que representa un mensaje de chat a almacenar en la base de datos.
            No tiene valor de retorno.
        """

        self.log_this(f" | --> [ Añadiendo ] {data} a la base de datos")

        try:
            # Establece la conexion
            with sqlite3.connect('mi_base_de_datos.db') as conexion:
                cursor = conexion.cursor()
                res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat';") # Selecionando la tabla a insertar
                cursor.execute("INSERT INTO chat(hora, usuario, texto) VALUES (?,?,?)", data) # Insertando datos
                conexion.commit()
        except Exception as dberror:
            self.log_this(f"| --> [ DATABASE SAVE ERROR ] \n{dberror}")
        else:
            self.log_this(f"    | --> Añadido ✔ a la base de datos")

    def clear_db(self):
        """ Borra todos los mensajes de la base de datos. No recibe argumentos ni devuelve valor. """

        self.log_this(f" | --> [ CLEANING DATABASE ] ")

        try:
            # Establece la conexion
            with sqlite3.connect('mi_base_de_datos.db') as conexion:
                cursor = conexion.cursor()            
                cursor.execute("DROP TABLE IF EXISTS chat") # Borra la tabla chat si existe
            self.mensajes = [] # Limpia la lista
        except Exception as dberror:
            self.log_this(f"| --> [ DATABASE SAVE ERROR ] \n{dberror}")
        finally:
            self.log_this(f"    | --> ✔ Base de datos limpiada.")

    def send_msgs(self, target, text_to_send: list):
        """
            Envía mensajes a un cliente recién conectado.
            Args:
                target (socket): El socket del cliente al que se enviarán los mensajes.
            No tiene valor de retorno.
        """

        try:
            for mensaje in text_to_send:
                serialized_data = dumps(mensaje)
                sleep(0.20)
                target.send(serialized_data)
        except BrokenPipeError as bpe:
            print(f"[ BrokenPipeError ] {bpe}")
            self.log_this(f"[ BrokenPipeError ] {bpe}")

def main():
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

        server_address = (ipv4_address, port)
    except ValueError as ve:
        print(f"Error {ve}")
        print("""Informacación incorrecta, asegurate que tener un formato correcto o prueba con otro puerto. Ej:
            IPv4 address: 127.0.0.1
            Port: 12345""")
    except KeyboardInterrupt:
        print("\nbye.")
    else:
        try:
            with socketserver.ThreadingTCPServer(server_address, ServidorChat) as server:
                print("Servidor en ejecución...")
                server.serve_forever()
        except KeyboardInterrupt:
            print("\nBye.")
        except Exception as e:
            print(f"Error {e}")
            print("""Something get wrong while creating server object, maybe you didn't put correcty the data. Here's an example:
                IPv4 address: 127.0.0.1
                Port: 12345
                        
            Or try another port.
            Try again. """)

if __name__=="__main__":
    main()