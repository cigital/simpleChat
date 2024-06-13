<p align="center">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M208 352c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176c0 38.6 14.7 74.3 39.6 103.4c-3.5 9.4-8.7 17.7-14.2 24.7c-4.8 6.2-9.7 11-13.3 14.3c-1.8 1.6-3.3 2.9-4.3 3.7c-.5 .4-.9 .7-1.1 .8l-.2 .2 0 0 0 0C1 327.2-1.4 334.4 .8 340.9S9.1 352 16 352c21.8 0 43.8-5.6 62.1-12.5c9.2-3.5 17.8-7.4 25.3-11.4C134.1 343.3 169.8 352 208 352zM448 176c0 112.3-99.1 196.9-216.5 207C255.8 457.4 336.4 512 432 512c38.2 0 73.9-8.7 104.7-23.9c7.5 4 16 7.9 25.2 11.4c18.3 6.9 40.3 12.5 62.1 12.5c6.9 0 13.1-4.5 15.2-11.1c2.1-6.6-.2-13.8-5.8-17.9l0 0 0 0-.2-.2c-.2-.2-.6-.4-1.1-.8c-1-.8-2.5-2-4.3-3.7c-3.6-3.3-8.5-8.1-13.3-14.3c-5.5-7-10.7-15.4-14.2-24.7c24.9-29 39.6-64.7 39.6-103.4c0-92.8-84.9-168.9-192.6-175.5c.4 5.1 .6 10.3 .6 15.5z"/></svg>
</p>
<p align="center">
    <h1 align="center">CHAT SIMPLE</h1>
</p>
<p align="center">
    Un proyecto de chat cliente-servidor local básico.
</p>
<p align="center">
	<!-- ![GitHub License](https://img.shields.io/github/license/cigital/simpleChat -->
	<img src="https://img.shields.io/github/license/cigital/simpleChat?style=flat-square">
	<img src="https://img.shields.io/github/last-commit/cigital/simpleChat?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/cigital/simpleChat?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/cigital/simpleChat?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLA DE CONTENIDOS -->
<details>
  <summary>Tabla de contenidos</summary><br>

- [ Visión General](#visión-general)
- [ Características](#características)
- [ Estructura del Repositorio](#estructura-del-repositorio)
- [ Archivos](#archivos)
- [ Empezando](#empezando)
  - [ Instalación](#instalación)
  - [ Uso](#uso)
- [ Hoja de Ruta del Proyecto](#hoja-de-ruta-del-proyecto)
- [ Contribuciones](#contribuciones)
- [ Licencia](#licencia)
- [ Referencias](#referencias)
</details>
<hr>

##  Visión general

El proyecto simpleChat consta de dos scripts de Python: uno para el cliente y otro para el servidor de un chat. El cliente se conecta al servidor utilizando sockets y permite a los usuarios enviar y recibir mensajes en una interfaz de línea de comandos. El servidor gestiona las conexiones de los clientes, almacena los mensajes en una base de datos SQLite y ofrece funcionalidades de control, como ver la lista de clientes conectados y enviar mensajes globales.

---

##  Características

- Permite la comunicación bidireccional entre múltiples clientes y un servidor.
- Almacena los mensajes en una base de datos SQLite para persistencia.
- Ofrece funcionalidades de control, como ver la lista de clientes conectados y enviar mensajes globales desde el servidor.

---


##  Estructura del repositorio

```sh
└── simpleChat/
    ├── client.py
    └── server.py
```

## Archivos

<details closed><summary>Descripción archivos</summary>

| Archivo                                                                   | Resumen                         |
| ---                                                                       | ---                             |
| [cliente.py](https://github.com/cigital/simpleChat/blob/master/client.py) | ► El archivo el qual deberá ejecutar el usuario para actuar como client.</code> |
| [servidor.py](https://github.com/cigital/simpleChat/blob/master/server.py) | ► El archivo el qual se debe ejecutar primero para tener el servidor activo. |

</details>

---

## Empezando

**Requisitos del sistema:**

* **Versión de Python testeada**: `3.10.12`

### Instalación

<h4>Desde <code>fuente</code></h4>

> 1. Clona el repositorio de simpleChat tanto en el dispositivo servidor como cliente:
>
> ```console
> $ git clone https://github.com/cigital/simpleChat
> ```
> 2. Cambia al directorio del proyecto:
> ```console
> $ cd simpleChat
> ```

### Uso

<h4>Desde <code>fuente</code></h4>

> Ejecuta el archivo del servidor desde el dispositivo que actuara como servidor, usando el siguiente comando:
> ```console
> $ python3 servidor.py
> ```
> Introduce los datos que te vaya pidiendo, como la adreça ip de destino al qual escuchar.

> Desde en el dispositvo cliente ejecute el archivo de cliente, con:
> ```console
> $ python3 client.py
> ```
> Introduce los datos que te vaya pidiendo, como la adreça ip de destino i el puerto, del servidor.

También podemos pasar argumentos (IP y puertos) de la siguiente manera:
- **miniServer.py**:
  ```console
  $ python3 [nombreArchivo].py --ip [=ip_a_escuchar | ip_a_escuchar] --port [=puerto_a_escuchar | puerto_a_escuchar]

Las opciones que hay són:
- **--ip**: Especifica la dirección IP en la que el servidor estará escuchando conexiones. Puede proporcionarse tanto en formato de argumento de línea de comandos (--ip=127.0.0.1) como en formato de valor de argumento (--ip 127.0.0.1).
- **--port**: Define el puerto en el que el servidor estará escuchando conexiones. Al igual que --ip, puede proporcionarse tanto en formato de argumento de línea de comandos (--port=123456) como en formato de valor de argumento (--port 123456).

---


## Hoja de ruta del proyecto

- [X] ► Añadir funcionalidad de chat
- [ ] ► Añadir funcionalidad de enviar imágenes
- [ ] ► Encriptación básica del chat

---

## Contribuciones
En este momento, no estamos aceptando contribuciones adicionales. ¡Gracias por tu interés!

</details>

---

## Licencia

Este proyecto está protegido bajo la licencia MIT. Para obtener más detalles, consulte el archivo [LICENSE](LICENSE).

---

## Referencias
A continuación tenemos páginas donde podemos profundizar mas para entender cómo funciona el codigo:
- [Documentación Socketserver](https://docs.python.org/3/library/socketserver.html)
- [Documentación Socket](https://docs.python.org/3/library/socket.html)
- [Documentación SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Documentación Threading](https://docs.python.org/3/library/threading.html)
- [Documentación Pickle](https://docs.python.org/3/library/pickle.html)

[**Volver arriba**](#-resumen)

---
