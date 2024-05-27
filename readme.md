<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">SIMPLECHAT</h1>
</p>
<p align="center">
    <em><code>Un proyecto de chat cliente-servidor básico.</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/cigital/simpleChat?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/cigital/simpleChat?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/cigital/simpleChat?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/cigital/simpleChat?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLA DE CONTENIDOS -->
<details>
  <summary>Tabla de Contenidos</summary><br>

- [ Visión General](#-visión-general)
- [ Características](#-características)
- [ Estructura del Repositorio](#-estructura-del-repositorio)
- [ Módulos](#-módulos)
- [ Empezando](#-empezando)
  - [ Instalación](#-instalación)
  - [ Uso](#-uso)
  - [ Pruebas](#-pruebas)
- [ Hoja de Ruta del Proyecto](#-hoja-de-ruta-del-proyecto)
- [ Contribuciones](#-contribuciones)
- [ Licencia](#-licencia)
- [ Agradecimientos](#-agradecimientos)
</details>
<hr>

##  Visión General

<code> El proyecto simpleChat consta de dos scripts de Python: uno para el cliente y otro para el servidor de un chat. El cliente se conecta al servidor utilizando sockets y permite a los usuarios enviar y recibir mensajes en una interfaz de línea de comandos. El servidor gestiona las conexiones de los clientes, almacena los mensajes en una base de datos SQLite y ofrece funcionalidades de control, como ver la lista de clientes conectados y enviar mensajes globales. En resumen, el proyecto proporciona una plataforma básica de chat cliente-servidor con capacidades de gestión y control. </code>

---

##  Características

- Permite la comunicación bidireccional entre múltiples clientes y un servidor.
- Almacena los mensajes en una base de datos SQLite para persistencia.
- Ofrece funcionalidades de control, como ver la lista de clientes conectados y enviar mensajes globales desde el servidor.

---


##  Estructura del Repositorio

```sh
└── simpleChat/
    ├── client.py
    └── server.py
```

## Archivos

<details closed><summary>Abreme</summary>

| Archivo                                                                   | Resumen                         |
| ---                                                                       | ---                             |
| [cliente.py](https://github.com/cigital/simpleChat/blob/master/client.py) | <code>► INSERTAR-TEXTO-AQUÍ</code> |
| [servidor.py](https://github.com/cigital/simpleChat/blob/master/server.py) | <code>► INSERTAR-TEXTO-AQUÍ</code> |

</details>

---

## Comenzando

**Requisitos del sistema:**

* **Versión de Python testeada**: `versión x.y.z`

### Instalación

<h4>Desde <code>fuente</code></h4>

> 1. Clona el repositorio de simpleChat:
>
> ```console
> $ git clone https://github.com/cigital/simpleChat
> ```
>
> 2. Cambia al directorio del proyecto:
> ```console
> $ cd simpleChat
> ```
>
> 3. Instala las dependencias:
> ```console
> $ pip install -r requirements.txt
> ```

### Uso

<h4>Desde <code>fuente</code></h4>

> Ejecuta simpleChat usando el siguiente comando:
> ```console
> $ python main.py
> ```

### Pruebas

> Ejecuta la suite de pruebas utilizando el siguiente comando:
> ```console
> $ pytest
> ```

---

## Hoja de ruta del proyecto

- [X] `► Añadir funcionalidad de chat`
- [ ] `► Añadir funcionalidad de enviar imágenes`
- [ ] `► Encriptación básica del chat`

---

## Contribuciones

¡Las contribuciones son bienvenidas! Aquí hay varias formas en las que puedes contribuir:

- **[Reportar Problemas](https://github.com/cigital/simpleChat/issues)**: Informa de errores encontrados o registra solicitudes de funciones para el proyecto `simpleChat`.
- **[Enviar Solicitudes de Extracción](https://github.com/cigital/simpleChat/blob/main/CONTRIBUTING.md)**: Revisa las solicitudes de extracción abiertas y envía tus propias solicitudes de extracción.
- **[Unirse a las Discusiones](https://github.com/cigital/simpleChat/discussions)**: Comparte tus ideas, proporciona comentarios o haz preguntas.

<details closed>
<summary>Directrices para Contribuir</summary>

1. **Clona el Repositorio**: Comienza por hacer un "fork" del repositorio del proyecto en tu cuenta de GitHub.

2. **Clonar Localmente**: Clona el repositorio bifurcado en tu máquina local utilizando un cliente de git.
   ```sh
   git clone https://github.com/cigital/simpleChat
   ```
3. **Crear una nueva rama**: Trabaje siempre en una nueva rama, dándole un nombre descriptivo.
   ```sh
   git checkout -b nueva-caracteristica-x
   ```
4. **Realice sus cambios**: desarrolle y pruebe sus cambios localmente.
5. **Confirma tus cambios**: confirma con un mensaje claro que describa tus actualizaciones.
    ```sh
    git commit -m 'Nueva característica implementada x.'
    ```
6. **Enviar a github**: envía los cambios a tu repositorio bifurcado.
    ```sh
    git push origen nueva-característica-x
    ```
7. **Envíe una solicitud de extracción**: cree un PR en el repositorio del proyecto original. Describe claramente los cambios y sus motivaciones.
8. **Revisión**: Una vez que su PR sea revisado y aprobado, se fusionará con la rama principal. ¡Felicitaciones por tu contribución!
</details>

---

## Licencia

Este proyecto está protegido bajo la licencia MIT. Para obtener más detalles, consulte el archivo [LICENSE](LICENSE).

---

## Agradecimientos

- Enumere aquí los recursos, contribuyentes, inspiración, etc.

[**Devolver**](#-resumen)

---
