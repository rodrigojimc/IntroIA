# Sistema RAG


Un sistema RAG (Retrieval-Augmented Generation) que integra la recuperación de documentos con la generación de respuestas con Gemini.
Está compuesto por un *backend* con FastAPI, ChromaDB como base de datos vectorial, Google AI para *embeddings* y generación de respuestas, y Streamlit para la UI.


## Características

- Soporta archivos en formato `.txt`, `.md` y `.pdf`.
- Identifica documentos relevantes para una pregunta y genera respuestas fundamentadas citando las fuentes de los documentos utilizados en la respuesta.
- Se rehúsa a responder si no hay suficiente evidencia en los documentos.
- ChromaDB persiste los *embeddings* en el disco.

## Generación y criterio de abstención

Para cada pregunta se recuperan los `top_k` *chunks* más similares (3 por defecto) y se decide si hay evidencia suficiente en dos pasos:

1. **Umbral de similitud (antes de llamar al modelo).** Se descartan los *chunks* con similitud coseno menor que `min_score = 0.3` (configurado en `app/main.py`). Si no queda ninguno, el sistema se abstiene **sin llamar a Gemini**.
2. **Criterio del modelo.** Los *chunks* que superan el umbral se incluyen en el *prompt* numerados `[1]`, `[2]`, … con su fuente. Se le indica a Gemini que responda en español, **solo** con esa evidencia, citando con `[n]`, sin añadir conocimiento externo, y que si el contexto no cubre la pregunta responda exactamente con el mensaje de abstención.

Cuando el sistema se abstiene, por cualquiera de los dos motivos:

- `answer` es: *"No tengo suficiente evidencia en los documentos para responder esta pregunta."*
- `abstained` es `true`.
- `citations` está vacío.

Cuando responde, `citations` contiene únicamente los *chunks* que se pasaron al modelo, con el mismo número `[n]` que aparece en la respuesta.

Los errores no se tratan como abstención: la API responde con un código HTTP de error y un campo `detail` con la descripción.

| Código | Causa |
|---|---|
| 404 | `/ingest`: el directorio no tiene archivos `.md`, `.txt` o `.pdf` |
| 422 | Pregunta vacía, o un archivo que no se pudo procesar |
| 500 | Error al leer o escribir en ChromaDB |
| 502 | Error de Google AI al generar *embeddings* o respuestas |
| 503 | `GOOGLE_API_KEY` no configurada |

## Requerimientos

- Python 3.10+
- Google AI API key

## Setup

### 1. Navega al directorio del proyecto

```bash
cd <parent-path>/rag-app
```

### 2. Crea un ambiente virtual

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura la API Key de Google AI 

1. Puedes obtener una gratuita en [Google AI Studio](https://aistudio.google.com/apikey).
2. Crea un archivo `.env`:

#### Copia la plantilla
```bash
cp .env.example .env
```

#### Edita .env y añade tu API key
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

**Importante**: 
Nunca subas el archivo `.env` al control de versiones. Ya está incluido en `.gitignore`.

### 5. Prepara tus Documentos

El sistema incluye documentos de ejemplo en el directorio `data/` que abarcan temas de aprendizaje automático, redes neuronales, NLP, RAG, LLMs y computación cuántica.


Para usar tus propios documentos puedes:
1. Añadir archivos `.txt`, `.md` o `.pdf` al directorio `data/`.
2. Ponerlos en otro directorio y escribir su ruta en la UI antes de pulsar *Cargar*.

## Ejecución

### Terminal 1: Inicia FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Debes ver algo como en la consola:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
...
INFO:     Application startup complete.
```
Visita http://127.0.0.1:8000/health para comprobar que el *backend* está corriendo correctamente. Deberías ver un mensaje de éxito:
```json
{"api_configured":true}
```
Puedes revisar la documentación de la API en: `http://localhost:8000/docs`

### Terminal 2: Inicia Streamlit

```bash
streamlit run ui/streamlit_app.py
```

Si es la primera vez que ejecutas Streamlit, verás un mensaje de bienvenida en la consola:
```
      Welcome to Streamlit!

      If you'd like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank.

      Email: 
```

Presiona *Enter* para continuar a la UI. 

Debes ver algo como:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

Si no se abre automáticamente en el navegador dirígete a http://localhost:8501

## Uso

1. En la barra lateral, escribe el directorio donde están los documentos (por defecto `data`) y pulsa *Cargar*. Debajo aparece la lista de documentos cargados.
2. Escribe tu pregunta y presiona *Enter* o pulsa *Buscar*.
3. La respuesta aparece debajo del botón. Expande *Fuentes* para ver los fragmentos citados y su similitud.

Solo se muestra la última pregunta con su respuesta: cada búsqueda nueva reemplaza la anterior.