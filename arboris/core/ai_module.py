"""
ARBORIS - AI Module
Integración con Groq API para sugerencias inteligentes
"""
import os
import json
from typing import Optional, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
ENV_EXAMPLE_PATH = os.path.join(BASE_DIR, ".env.example")

try:
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH)
    if not os.getenv("GROQ_API_KEY"):
        load_dotenv(ENV_EXAMPLE_PATH)
except ImportError:
    pass

try:
    from groq import Groq
except ImportError:
    Groq = None

MODEL_CANDIDATES = ("llama-3.3-70b-versatile", "llama-3.1-8b-instant")
PLACEHOLDER_KEYS = {"", "your-groq-key-here"}


def get_api_key() -> str:
    return (os.getenv("GROQ_API_KEY") or "").strip()


def get_client() -> Optional[Any]:
    if Groq is None:
        return None
    key = get_api_key()
    if key in PLACEHOLDER_KEYS:
        return None
    return Groq(api_key=key)


def get_ai_unavailable_message() -> str:
    if Groq is None:
        return "Dependencia faltante. Instala groq>=0.9.0"
    key = get_api_key()
    if not key:
        return "GROQ_API_KEY no encontrada. Crea .env o agrega la clave en .env.example"
    if key == "your-groq-key-here":
        return "GROQ_API_KEY sigue con el valor de ejemplo. Reemplazala por tu clave real"
    return "No se pudo inicializar el cliente de Groq"


def create_chat_completion(client: Any, prompt: str, max_tokens: int) -> Any:
    last_error = None
    for model in MODEL_CANDIDATES:
        try:
            return client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:
            last_error = exc
    raise last_error if last_error else RuntimeError("No se pudo obtener respuesta de Groq")


def suggest_task_attributes(description: str) -> Dict[str, Any]:
    """
    Dado un texto libre, la IA sugiere: título, prioridad, etiquetas, fecha y notas.
    Retorna dict con los atributos sugeridos.
    """
    client = get_client()
    if not client:
        return {
            "title": description[:60],
            "priority": "media",
            "tags": [],
            "due_date": None,
            "notes": "",
            "error": get_ai_unavailable_message(),
        }

    prompt = f"""Analiza esta descripción de tarea y responde SOLO con un JSON válido (sin markdown, sin texto extra):

Descripción: "{description}"

Responde con este esquema exacto:
{{
  "title": "título corto y claro (max 60 chars)",
  "priority": "alta|media|baja",
  "tags": ["etiqueta1", "etiqueta2"],
  "due_date": "YYYY-MM-DD o null si no se menciona fecha",
  "notes": "notas adicionales relevantes o string vacío",
  "node_type": "proyecto|tarea|subtarea|nota"
}}

Reglas:
- priority=alta si hay palabras como urgente, crítico, asap, hoy, ya
- priority=baja si dice cuando pueda, sin prisa, eventual
- Extrae fechas relativas asumiendo que hoy es {__import__('datetime').date.today()}
- tags: máximo 4, en minúsculas, relevantes al contenido"""

    try:
        response = create_chat_completion(client, prompt, max_tokens=400)
        text = response.choices[0].message.content.strip()
        # clean possible markdown fences
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception as e:
        return {
            "title": description[:60],
            "priority": "media",
            "tags": [],
            "due_date": None,
            "notes": "",
            "error": str(e),
        }


def generate_project_summary(project_data: Dict[str, Any]) -> str:
    """Genera un resumen ejecutivo del proyecto con IA"""
    client = get_client()
    if not client:
        return f"⚠️ {get_ai_unavailable_message()}"

    prompt = f"""Eres un asistente de gestión de proyectos. Genera un resumen ejecutivo conciso (máximo 150 palabras) del siguiente proyecto:

{json.dumps(project_data, ensure_ascii=False, indent=2)}

El resumen debe incluir:
1. Estado general del proyecto
2. Tareas críticas pendientes
3. Riesgos (tareas vencidas o de alta prioridad sin completar)
4. Recomendación de próximos pasos

Escribe en español, tono profesional pero directo."""

    try:
        response = create_chat_completion(client, prompt, max_tokens=300)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generando resumen: {e}"


def detect_duplicates(new_title: str, existing_titles: list) -> Optional[str]:
    """Detecta si la nueva tarea es duplicado de alguna existente"""
    client = get_client()
    if not client or not existing_titles:
        return None

    prompt = f"""¿El título "{new_title}" es semánticamente similar a alguno de estos títulos existentes?

Títulos existentes:
{chr(10).join(f'- {t}' for t in existing_titles[:30])}

Responde SOLO con JSON:
{{"is_duplicate": true/false, "similar_to": "título similar o null", "confidence": 0.0-1.0}}"""

    try:
        response = create_chat_completion(client, prompt, max_tokens=100)
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)
        if data.get("is_duplicate") and data.get("confidence", 0) > 0.8:
            return data.get("similar_to")
        return None
    except Exception:
        return None
