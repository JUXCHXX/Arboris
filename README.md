<div align="center">

```
 █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║██╔════╝
███████║██████╔╝██████╔╝██║   ██║██████╔╝██║███████╗
██╔══██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██║╚════██║
██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║██║███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝
```

**Gestión inteligente de tareas y proyectos potenciada por IA**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Claude AI](https://img.shields.io/badge/Claude-AI_Integrado-D4A27F?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![License](https://img.shields.io/badge/Licencia-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Estado-Activo-22C55E?style=flat-square)]()

*Organiza proyectos y tareas en estructuras de árbol n-ario con visualización en tiempo real,*
*inteligencia artificial integrada y herramientas de productividad.*

---

[📦 Instalación](#-instalación) · [🖥️ Interfaz](#%EF%B8%8F-interfaz) · [🤖 Funciones IA](#-funciones-de-ia) · [📤 Exportación](#-exportación) · [🛠️ Solución de Problemas](#%EF%B8%8F-solución-de-problemas)

</div>

---

## ✨ Características Principales

| | Característica | Descripción |
|---|---|---|
| 🌳 | **Árbol Visual Interactivo** | Visualiza proyectos y tareas como un grafo n-ario en tiempo real |
| 🤖 | **IA con Claude** | Sugiere tareas, infiere prioridades y genera resúmenes ejecutivos |
| 📊 | **Dashboard con Gráficas** | Circular, barras por prioridad y diagrama de Gantt integrado |
| ⏱️ | **Pomodoro Timer** | Temporizador integrado con notificaciones del sistema operativo |
| 📤 | **Exportación Múltiple** | Exporta a PDF, Excel o importa desde CSV |
| 🔍 | **Búsqueda y Filtros** | Filtra por título, prioridad y estado en tiempo real |
| 💾 | **Persistencia Automática** | Guardado automático en JSON sin intervención del usuario |
| 🔔 | **Alertas Inteligentes** | Notificaciones nativas para tareas vencidas y urgentes |

---

## ⚡ Inicio Rápido

```bash
# 1. Clonar/descomprimir y entrar al proyecto
cd arboris/

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key
cp .env.example .env
# → Abre .env y reemplaza: ANTHROPIC_API_KEY=sk-ant-TU-KEY-AQUÍ

# 4. ¡Ejecutar!
python main.py
```

> **¿Dónde obtengo mi API key?**
> Regístrate en [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key
>
> ⚠️ Sin API key la app funciona al 100%, pero las funciones de IA mostrarán un aviso.

---

## 📋 Requisitos

| Requisito | Versión mínima |
|-----------|:--------------:|
| Python | `3.10+` |
| Sistema Operativo | Windows / macOS / Linux |
| Graphviz (para árbol visual) | Cualquier versión estable |

---

## 🔧 Instalación Detallada

### 1 · Entrar al proyecto

```bash
cd arboris/
```

### 2 · Crear entorno virtual *(recomendado)*

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3 · Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4 · Configurar variables de entorno

```bash
cp .env.example .env
```

Abre `.env` con cualquier editor y completa:

```env
ANTHROPIC_API_KEY=sk-ant-TU-KEY-REAL-AQUÍ
```

### 5 · Ejecutar

```bash
python main.py
```

---

## 🖥️ Interfaz

```
┌─────────────────────────────────────────────────────────────────────┐
│  🌳 ARBORIS    [🔍 Buscar...]   [Prioridad ▼]  [Estado ▼]  [Exportar]│
├──────────────────┬──────────────────────────────────────────────────┤
│                  │                                                  │
│  ＋ Nuevo        │  ╔══════════════════════════════════════════════╗ │
│  ➕ Subtarea     │  ║  Tab: 🌳 Árbol  |  📊 Dashboard  |  📋 Detalle ║ │
│                  │  ╠══════════════════════════════════════════════╣ │
│  🤖 Describe tu  │  ║                                              ║ │
│     tarea...     │  ║    [Visualización principal según pestaña]   ║ │
│  ✨ Sugerir con IA│  ║                                              ║ │
│  ──────────────  │  ╚══════════════════════════════════════════════╝ │
│  📋 Lista de     │                                                  │
│     nodos        │                                                  │
│     (scroll)     │                                                  │
│                  │                                                  │
│  ⏱ POMODORO     │                                                  │
│  [▶] [↺] 25:00  │                                                  │
└──────────────────┴──────────────────────────────────────────────────┘
```

---

## 📖 Manual de Usuario

### Crear un Proyecto o Tarea

1. Haz clic en **＋ Nuevo Proyecto** para crear un nodo raíz.
2. Completa el formulario:

   | Campo | Opciones / Formato |
   |---|---|
   | **Título** | Texto libre *(obligatorio)* |
   | **Tipo** | `proyecto` / `tarea` / `subtarea` / `nota` |
   | **Prioridad** | `alta` / `media` / `baja` |
   | **Estado** | `pendiente` / `en progreso` / `completado` / `cancelado` |
   | **Fecha de vencimiento** | `YYYY-MM-DD` — ej: `2026-05-23` |
   | **Etiquetas** | Separadas por coma — ej: `backend, urgente, api` |
   | **Notas** | Texto libre |

3. Haz clic en **✓ Guardar**.

### Crear una Subtarea

1. Selecciona el nodo padre en la lista izquierda.
2. Haz clic en **➕ Subtarea** y completa el formulario.

> El nodo hijo quedará vinculado al padre en la jerarquía del árbol.

### Editar un Nodo

1. Selecciona el nodo → pestaña **📋 Detalle**.
2. Haz clic en **✏️ Editar**, modifica y guarda.

### Eliminar un Nodo

1. Selecciona el nodo → pestaña **📋 Detalle** → **🗑 Eliminar**.
2. Confirma en el diálogo.

> ⚠️ **Advertencia:** eliminar un nodo borra también todos sus nodos hijos en cascada.

### Buscar y Filtrar

- **🔍 Barra de búsqueda** — filtra por título o notas en tiempo real.
- **Prioridad ▼** — muestra solo nodos de una prioridad específica.
- **Estado ▼** — muestra solo nodos con un estado concreto.
- Los tres filtros son combinables entre sí.

---

## 🤖 Funciones de IA

> Todas las funciones de IA requieren una API key válida de Anthropic.

### Sugerir tarea con IA

1. En el panel izquierdo, escribe una descripción en lenguaje natural:
   ```
   "reunión urgente con el cliente sobre el presupuesto mañana viernes"
   ```
2. Haz clic en **✨ Sugerir con IA**.
3. La IA pre-rellenará automáticamente:
   - Título limpio y conciso
   - Prioridad inferida del contexto
   - Fecha de vencimiento extraída
   - Etiquetas relevantes
   - Tipo de nodo sugerido
4. Revisa, ajusta si quieres y guarda.

> 💡 La IA también detecta tareas duplicadas y te avisa antes de crear una nueva.

### Resumen ejecutivo *(IA)*

1. Selecciona cualquier nodo → pestaña **📋 Detalle**.
2. Haz clic en **🤖 Resumen IA**.
3. Obtendrás en segundos: estado general, tareas críticas, riesgos y recomendaciones.

---

## 🌳 Vista de Árbol

La pestaña **🌳 Árbol** muestra todos los nodos como un grafo interactivo.

| Color | Significado |
|:---:|---|
| 🔴 Rojo | Prioridad alta o tarea vencida |
| 🟡 Amarillo | Prioridad media |
| 🟢 Verde | Prioridad baja o tarea completada |

- **Clic en un nodo** del árbol → lo selecciona y abre su detalle.
- El árbol se actualiza automáticamente al crear, editar o eliminar nodos.

---

## 📊 Dashboard

La pestaña **📊 Dashboard** incluye tres gráficas en tiempo real:

```
┌─────────────────┬─────────────────┬─────────────────────────────┐
│  ◉ Circular     │  ▌ Por Prioridad │  ═══ Gantt (próx. 10)       │
│                 │                 │                             │
│  Completadas    │  Alta  ████░░   │  🔴 Tarea A   [======]      │
│  vs Pendientes  │  Media ██░░░░   │  🟡 Tarea B      [====]     │
│                 │  Baja  █░░░░░   │  🟢 Tarea C         [==]    │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

**Leyenda Gantt:**

| Color | Urgencia |
|:---:|---|
| 🔴 Rojo | Fecha ya vencida |
| 🟡 Amarillo | Vence en ≤ 3 días |
| 🟢 Verde/Teal | Tiempo suficiente |

---

## ⏱️ Pomodoro Timer

Ubicado en la parte inferior del panel izquierdo.

| Control | Acción |
|:---:|---|
| **▶ / ⏸** | Iniciar / Pausar el temporizador |
| **↺** | Reiniciar a 25 minutos |

- Alterna automáticamente entre **TRABAJO (25 min)** y **DESCANSO (5 min)**.
- Al terminar cada ciclo envía una **notificación nativa** del sistema operativo.

---

## 📤 Exportación

### Exportar a PDF

```
📤 Exportar PDF  →  Elegir ubicación  →  Guardar
```
El PDF incluye: resumen general, estadísticas y el árbol completo con jerarquía.

### Exportar a Excel

```
📊 Exportar Excel  →  Elegir ubicación  →  Guardar
```
Genera un `.xlsx` con todas las tareas tabuladas, coloreadas por prioridad y estado.

### Importar desde CSV

```
📥 Importar CSV  →  Seleccionar archivo  →  Las tareas se agregan como nodos raíz
```

**Formato CSV esperado:**

```csv
title,type,priority,due_date,tags,notes,status
Mi tarea,tarea,alta,2026-05-25,tag1;tag2,Notas aquí,pendiente
```

> Hay un archivo de ejemplo listo para usar en `sample_import.csv`.

---

## 💾 Persistencia de Datos

Los datos se guardan **automáticamente** en `data/arboris_data.json` cada vez que:

- Creas, editas o eliminas un nodo
- Importas desde CSV
- Cierras la aplicación

Al abrir ARBORIS, los datos se cargan automáticamente sin ninguna acción del usuario.

---

## 📁 Estructura del Proyecto

```
arboris/
│
├── 📄 main.py                  ← Punto de entrada
├── 📄 requirements.txt         ← Dependencias Python
├── 📄 .env.example             ← Plantilla de configuración
├── 📄 sample_import.csv        ← CSV de ejemplo para importar
│
├── 📂 core/
│   ├── tree.py                 ← Árbol n-ario (Node + ArborisTree)
│   ├── ai_module.py            ← Integración con Claude API
│   ├── exports.py              ← PDF, Excel, CSV
│   └── notifications.py        ← Alertas del sistema operativo
│
├── 📂 gui/
│   └── app.py                  ← Interfaz gráfica completa (customtkinter)
│
└── 📂 data/                    ← Generado automáticamente al ejecutar
    └── arboris_data.json       ← Base de datos local persistente
```

---

## 📦 Dependencias

| Librería | Versión | Uso |
|---|:---:|---|
| `customtkinter` | latest | GUI moderna con soporte dark mode |
| `matplotlib` | latest | Árbol visual + gráficas del dashboard |
| `networkx` | latest | Lógica del grafo del árbol |
| `anthropic` | latest | Claude API para funciones de IA |
| `fpdf2` | latest | Generación de reportes PDF |
| `openpyxl` | latest | Exportación a Excel |
| `python-dotenv` | latest | Carga de variables de entorno |
| `plyer` | latest | Notificaciones nativas del sistema operativo |

Instala todo de una vez:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Solución de Problemas

| Síntoma | Solución |
|---|---|
| `ModuleNotFoundError` | Ejecuta `pip install -r requirements.txt` |
| La IA no responde | Verifica que `.env` existe y contiene tu API key real |
| El árbol no se dibuja | Instala Graphviz del sistema (ver abajo) |
| Sin notificaciones en macOS | Ajustes → Notificaciones → Permite a Python |
| Error al exportar PDF | Verifica permisos de escritura en la carpeta destino |

**Instalar Graphviz:**

```bash
# Ubuntu / Debian
sudo apt install graphviz

# macOS (Homebrew)
brew install graphviz

# Windows → descarga en https://graphviz.org/download/
```

---

## 🔔 Notificaciones del Sistema

Al iniciar ARBORIS, se revisan todas las tareas automáticamente y se envían notificaciones nativas si:

- Existen tareas **vencidas** (fecha pasada, no completadas)
- Existen tareas que **vencen hoy**

---

<div align="center">

---

**ARBORIS** · Proyecto Académico de Estructuras de Datos

Desarrollado con Python 3.11+ · Mayo 2026

*"No entregues código. Entrega un producto."*

</div>