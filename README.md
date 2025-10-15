# LeafLink BOT - Asistente Virtual para E-commerce

<img src="static/LeafLink.png" alt="Logo" width="150" align="right" style="margin-left: 20px; margin-bottom: 20px;" />

[![Hybridge Education](https://img.shields.io/badge/Hybridge-Education-lightgrey)](https://www.hybridge.education)

![Flask](https://img.shields.io/badge/Flask-2.3.3-blue) ![pandas](https://img.shields.io/badge/pandas-2.3.3-green) ![openai](https://img.shields.io/badge/openai-0.28.1-orange) ![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.0-purple) ![numpy](https://img.shields.io/badge/numpy-2.3.3-red)

## Descripción

**LeafLink BOT** es un proyecto académico que demuestra la implementación de un asistente conversacional (chatbot) basado en un Large Language Model (LLM) en una página web de e-commerce ficticia. La plataforma web, desarrollada con **Flask** y **Tailwind CSS**, simula una tienda en línea de plantas y productos de aromaterapia. El chatbot, impulsado por la API de **OpenAI (GPT-3.5-turbo)**, está diseñado para responder preguntas de los clientes basándose en la información de un catálogo de productos, mejorando así la experiencia de usuario y la eficiencia del servicio al cliente.

![Navegación en la página web de LeafLink](Screenshots/navegacion_pagina_web_scroll.gif)
*Figura 1: Demostración de la navegación fluida y el diseño responsivo de la página principal de LeafLink.*

---

## Sobre LeafLink: Nuestra Historia

**LeafLink** es una marca concebida para conectar a las personas con la naturaleza y el bienestar. Fundada en 2022 en San Pedro Garza García, Nuevo León, por la diseñadora industrial **Sofía Martínez** y el horticultor urbano **Diego Hernández**, LeafLink nació del sueño de acercar la naturaleza a la vida cotidiana. Lo que comenzó como un pequeño estudio de venta de plantas, rápidamente floreció gracias a un fuerte compromiso con la calidad y la educación sobre el cuidado de las plantas.

Nuestra **misión** es *"Llevar bienestar natural a cada hogar a través de plantas, accesorios y experiencias que inspiren conexión con la tierra"*. Operamos como una tienda en línea y un club de suscripción, ofreciendo una cuidada selección de plantas de interior, kits de jardinería, difusores de aceites esenciales y accesorios de decoración.

Para conocer más a fondo la identidad, los valores y la visión de nuestra marca, te invitamos a consultar nuestro manual de identidad corporativa en el archivo **[leaflink_brand_manual.pdf](leaflink_brand_manual.pdf)**.

---

## 🎯 Características

-   **Interfaz de E-commerce Atractiva:** Página web desarrollada con Flask y estilizada con Tailwind CSS, ofreciendo un diseño moderno y responsivo.
-   **Asistente Virtual Inteligente:** Chatbot integrado que utiliza `gpt-3.5-turbo` para proporcionar respuestas precisas y contextuales sobre los productos.
-   **Catálogo Dinámico:** El chatbot consulta un catálogo en formato CSV para obtener información en tiempo real sobre productos, precios y stock.
-   **Filtrado Inteligente de Relevancia:** El backend filtra y envía solo los productos más relevantes al LLM para optimizar el contexto y la precisión de la respuesta.
-   **Manejo de Preguntas Fuera de Contexto:** El asistente está instruido para declinar amablemente preguntas que no están relacionadas con el catálogo de productos.
-   **Soporte Multilingüe:** La página web cuenta con un selector para cambiar entre español e inglés.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura cliente-servidor simple pero robusta, donde el frontend interactúa con un backend en Flask que orquesta la lógica del negocio y la comunicación con la API de OpenAI.

1.  **Frontend (Cliente):** El usuario interactúa con la página web y el widget del chatbot. Las preguntas se envían al backend a través de peticiones `POST` asíncronas (AJAX).
2.  **Backend (Servidor Flask):**
    * Recibe la pregunta del usuario desde el endpoint `/chat`.
    * Carga el catálogo de productos desde el archivo `leaflink_catalogo.csv` utilizando la librería `pandas`.
    * Filtra los productos más relevantes para la pregunta del usuario con el fin de optimizar el `prompt` enviado a la IA.
    * Construye un `prompt` detallado que incluye las instrucciones para el LLM y el contexto del catálogo filtrado.
    * Envía el `prompt` a la API de **OpenAI**.
    * Recibe la respuesta generada por el modelo `gpt-3.5-turbo`.
    * Retorna la respuesta al frontend en formato JSON.
3.  **OpenAI (LLM):** El modelo de lenguaje procesa el `prompt` y genera una respuesta en lenguaje natural siguiendo las instrucciones proporcionadas.

```mermaid
graph TD
    subgraph "Cliente (Navegador Web)"
        A["🌐 Usuario"] -->|Interactúa con| B["💻 Interfaz Web - HTML/CSS/JS"]
        B -->|1. Envía pregunta| C["🤖 Chatbot Widget"]
        C -->|2. Petición POST a /chat| D["🐍 Backend (Flask)"]
    end

    subgraph "Servidor"
        D -->|3. Carga catálogo| E["📄 leaflink_catalogo.csv"]
        D -->|4. Filtra productos relevantes| E
        D -->|5. Construye Prompt| F["🧠 OpenAI API"]
        F -->|6. Recibe respuesta| D
    end

    subgraph "OpenAI"
        F <-->|Genera texto| G["🤖 gpt-3.5-turbo"]
    end

    D -->|7. Devuelve JSON con respuesta| C
    C -->|8. Muestra respuesta| A
````

*Figura 2: Diagrama de la arquitectura del proyecto LeafLink, mostrando el flujo de interacción desde el usuario hasta la respuesta del asistente de IA.*

-----

## 🧪 Pruebas del Chatbot

A continuación, se muestran algunas capturas de pantalla que demuestran el funcionamiento y las capacidades del asistente virtual.

| Inicio del Chat | Saludo Inicial | Consulta de Precio y Stock | Consulta de Producto Específico | Pregunta Fuera de Alcance |
| :---: | :---: | :---: | :---: | :---: |
| ![Inicio del Chat](<Screenshots/bot_inicio.png>) | ![Saludo Inicial](<Screenshots/bot_enviar_hola.png>) | ![Consulta de Precio y Stock](<Screenshots/bot_Cuál es el precio en MXN y el stock disponible de la planta Lengua de suegra.png>) | ![Consulta de Producto Específico](<Screenshots/bot_Qué producto de aromaterapia en formato difusor tienen y cuál es su precio.png>) | ![Pregunta Fuera de Alcance](<Screenshots/bot_Venden fertilizante orgánico líquido para plantas de interior.png>) |
| *Figura 3: Estado inicial del chatbot al cargar la página.* | *Figura 4: Respuesta del bot a un saludo simple.* | *Figura 5: El bot proporciona datos precisos del catálogo.* | *Figura 6: El bot identifica y describe un producto específico.* | *Figura 7: El bot maneja correctamente preguntas sobre productos no existentes en el catálogo.*|

-----

## 📂 Estructura del Repositorio

```
.
├── app.py                  # Archivo principal de la aplicación Flask
├── leaflink_catalogo.csv   # Catálogo de productos
├── leaflink_brand_manual.pdf # Manual de identidad de la marca
├── requirements.txt        # Dependencias de Python
├── static/                 # Carpeta para archivos estáticos (CSS, JS, imágenes)
│   ├── logo.png
│   ├── producto-monstera.jpg
│   └── ...
├── templates/              # Carpeta para las plantillas HTML
│   └── index.html
├── Screenshots/            # Capturas de pantalla del proyecto
│   ├── pantalla_principal.png
│   ├── navegacion_pagina_web_scroll.gif
│   └── ...
├── .gitignore              # Archivos y carpetas a ignorar por Git
└── README.md               # Este archivo
```

-----

## ⚙️ Instalación

Sigue estos pasos para clonar y ejecutar el proyecto en tu máquina local.

### Prerrequisitos

  - Python 3.8 o superior
  - Git
  - Una clave de API de OpenAI

### Pasos Generales

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/jesusvasquezjr3/LeafLink.git](https://github.com/jesusvasquezjr3/LeafLink.git)
    cd LeafLink
    ```

2.  **Crear y activar un entorno virtual:**

      * **Windows (Command Prompt):**

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

      * **Windows (PowerShell):**

        ```bash
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        ```

      * **macOS / Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno:**

      * Crea un archivo llamado `.env` en la raíz del proyecto.
      * Añade tu clave de API de OpenAI al archivo de la siguiente manera:
        ```
        OPENAI_API_KEY='tu_clave_de_api_aqui'
        ```

5.  **Ejecutar la aplicación:**

    ```bash
    flask run
    ```

    O alternativamente:

    ```bash
    python app.py
    ```

6.  **Abrir en el navegador:**
    Abre tu navegador web y ve a `http://127.0.0.1:5000` para ver la aplicación en funcionamiento.

---

> The development of this application corresponds to the subject of **Artificial Intelligence** in [Hybridge Education](https://www.hybridge.education).
