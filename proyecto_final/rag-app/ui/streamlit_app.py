import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Sistema RAG", layout="wide", initial_sidebar_state="expanded")

API_BASE_URL = "http://localhost:8000"

if "last_item" not in st.session_state:
    st.session_state.last_item = None

def check_api_health() -> tuple[bool, dict | None]:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException:
        return False, None

def error_detail(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
    except ValueError:
        detail = None
    # Los errores de validación de FastAPI (422) traen una lista en lugar de un texto
    return detail if isinstance(detail, str) else f"Error {response.status_code}"

def ingest_directory(dir_path: str) -> str | None:
    """Devuelve None si la carga fue bien, o el mensaje de error."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ingest",
            json={"directory_path": dir_path},
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        return f"No se pudo conectar con la API: {e}"
    return None if response.ok else error_detail(response)

def list_documents() ->  list[str]:
    try:
        response = requests.get(f"{API_BASE_URL}/documents", timeout=10)
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            return [doc["name"] for doc in documents]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def query_rag(question: str, top_k: int = 3) -> tuple[dict | None, str | None]:
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question, "top_k": top_k},
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        return None, f"No se pudo conectar con la API: {e}"
    if not response.ok:
        return None, error_detail(response)
    return response.json(), None

st.title("Sistema RAG")
st.markdown("Retrieval Augmented Generation")

api_ok, health_info = check_api_health()

if not api_ok:
    st.error("Inicia el servidor FastAPI: uvicorn app.main:app --reload --port 8000")
    st.stop()

if health_info and not health_info.get("api_configured"):
    st.warning("API key no configurada.")

with st.sidebar:
    st.header("Documentos")
    dir_path = st.text_input("Directorio:", value="data")
    st.markdown("<small>Soporta archivos en formato .txt, .md y .pdf</small>", unsafe_allow_html=True)
    if st.button("Cargar", use_container_width=True):
        with st.spinner("Cargando documentos..."):
            error = ingest_directory(dir_path)
            if error:
                st.error(f"Error al cargar documentos: {error}")
            else:
                st.success("Documentos cargados")

    documents = list_documents()
    if documents:
        st.markdown(f"**Documentos cargados ({len(documents)})**")
        for doc in documents:
            st.markdown(f"- {doc}")

with st.form("query_form", border=False, clear_on_submit=True):
    question = st.text_input(
        "Pregunta:",
        placeholder="¿Qué te gustaría saber?"
    )
    submit_button = st.form_submit_button("Buscar", use_container_width=True)

if submit_button:
    if not question or len(question.strip()) == 0:
        st.warning("Escribe una pregunta")
    else:
        with st.spinner("Buscando..."):
            result, error = query_rag(question)

        if error:
            st.session_state.last_item = None
            st.error(error)
        else:
            st.session_state.last_item = {
                "question": question,
                "answer": result["answer"],
                "citations": result["citations"],
                "abstained": result["abstained"]
            }

item = st.session_state.last_item
if item:
    st.chat_message("user").write(item["question"])

    with st.chat_message("assistant"):
        if item["abstained"]:
            st.warning(item["answer"])
        else:
            st.write(item["answer"])

        if item["citations"]:
            with st.expander(f"Fuentes ({len(item['citations'])} documentos citados)"):
                for citation in item["citations"]:
                    st.markdown(f"**[{citation['id']}] {citation['source']}** (similitud: {citation['score']:.3f})")
                    st.text(citation["text"][:400] + "..." if len(citation["text"]) > 400 else citation["text"])
                    st.divider()

st.divider()
st.markdown("""
### Cómo usar:
1. Escribe el directorio en donde se encuentran los documentos y haz click en *Cargar*
2. Escribe tu pregunta en la caja de texto y presiona *Enter* o haz click en *Buscar*
3. Expande la sección *Fuentes* debajo de cada respuesta para revisar los documentos citados.
""")