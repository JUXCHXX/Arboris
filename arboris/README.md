# 🌳 ARBORIS
### Gestión inteligente de tareas y proyectos con IA

> Aplicación de escritorio Python que organiza proyectos y tareas en una estructura de árbol n-ario, con interfaz moderna, inteligencia artificial integrada, visualización en tiempo real y herramientas de productividad.

---

## ⚡ Inicio Rápido (3 comandos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear archivo .env con tu API key
cp .env.example .env
# → Abre .env y reemplaza sk-ant-your-key-here con tu key real

# 3. Ejecutar
python main.py
```

---

## 📋 Requisitos

| Requisito | Versión mínima |
|-----------|----------------|
| Python    | 3.10+          |
| Sistema   | Windows / macOS / Linux |

---

## 🔧 Instalación Detallada

### 1. Clonar o descomprimir el proyecto

```bash
cd arboris/
```

### 2. (Recomendado) Crear entorno virtual

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Crear .env desde la plantilla
cp .env.example .env
```

Abre el archivo `.env` con cualquier editor de texto y reemplaza el valor:

```env
ANTHROPIC_API_KEY=sk-ant-TU-KEY-REAL-AQUÍ
```

> **¿Dónde obtengo mi API key?**
> Regístrate en [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key
>
> ⚠️ Sin API key la app funciona al 100%, pero las funciones de IA mostrarán un aviso.

### 5. Ejecutar

```bash
python main.py
```

---

## 🖥️ Interfaz — Guía Visual

```
┌─────────────────────────────────────────────────────────────────┐
│  🌳 ARBORIS   [🔍 Buscar]  [Prioridad ▼]  [Estado ▼]  [Exportar] │  ← Barra superior
├────────────────┬────────────────────────────────────────────────┤
│                │                                                │
│  ＋ Nuevo      │   Tab: 🌳 Árbol  |  📊 Dashboard  |  📋 Detalle │
│  ➕ Subtarea   │                                                │
│                │   [Visualización principal según pestaña]      │
│  🤖 IA input   │                                                │
│  ────────────  │                                                │
│  Lista de      │                                                │
│  nodos         │                                                │
│  (scrollable)  │                                                │
│                │                                                │
│  ⏱ POMODORO   │                                                │
└────────────────┴────────────────────────────────────────────────┘
```

---

## 📖 Manual de Usuario

### Crear un Proyecto o Tarea

1. Haz clic en **＋ Nuevo Proyecto** (panel izquierdo) para crear un nodo raíz.
2. Se abrirá un formulario con los campos:
   - **Título** *(obligatorio)*
   - **Tipo**: proyecto / tarea / subtarea / nota
   - **Prioridad**: alta / media / baja
   - **Estado**: pendiente / en progreso / completado / cancelado
   - **Fecha de vencimiento**: formato `YYYY-MM-DD` (ej: `2026-05-23`)
   - **Etiquetas**: separadas por coma (ej: `backend, urgente, api`)
   - **Notas**: texto libre
3. Haz clic en **✓ Guardar**.

### Crear una Subtarea

1. Selecciona primero el nodo padre en la lista de la izquierda.
2. Haz clic en **➕ Subtarea**.
3. Completa el formulario y guarda.

> El nodo hijo quedará vinculado al padre en el árbol.

### Editar un Nodo

1. Selecciona el nodo (clic en la lista o en el árbol visual).
2. Ve a la pestaña **📋 Detalle**.
3. Haz clic en **✏️ Editar**.
4. Modifica los campos y guarda.

### Eliminar un Nodo

1. Selecciona el nodo.
2. En la pestaña **📋 Detalle**, haz clic en **🗑 Eliminar**.
3. Confirma en el diálogo.

> ⚠️ Eliminar un nodo borra también todos sus hijos.

### Buscar y Filtrar

- **Barra de búsqueda** (arriba): filtra por título o contenido de notas en tiempo real.
- **Dropdown Prioridad**: muestra solo los nodos de esa prioridad.
- **Dropdown Estado**: muestra solo los nodos con ese estado.
- Los filtros se pueden combinar entre sí.

---

## 🤖 Funciones de Inteligencia Artificial

### Sugerir tarea con IA

1. En el panel izquierdo, escribe una descripción en lenguaje natural en el campo **"IA — Describe tu tarea"**.
   - Ejemplo: *"reunión urgente con el cliente sobre el presupuesto mañana viernes"*
2. Haz clic en **✨ Sugerir con IA**.
3. La IA analizará tu texto y pre-rellenará el formulario con:
   - Título limpio y conciso
   - Prioridad inferida del contexto
   - Fecha de vencimiento extraída
   - Etiquetas relevantes
   - Tipo de nodo sugerido
4. Revisa, ajusta si quieres y guarda.

> La IA también detecta si la tarea es similar a una existente y te avisa antes de crear un duplicado.

### Resumen ejecutivo de proyecto (IA)

1. Selecciona cualquier nodo (proyecto o tarea).
2. Ve a la pestaña **📋 Detalle**.
3. Haz clic en **🤖 Resumen IA**.
4. En segundos aparecerá un análisis con: estado general, tareas críticas, riesgos y recomendaciones.

---

## 🌳 Vista de Árbol

La pestaña **🌳 Árbol** muestra todos los nodos y sus relaciones como un grafo interactivo:

| Color del nodo | Significado |
|----------------|-------------|
| 🔴 Rojo        | Prioridad alta o tarea vencida |
| 🟡 Amarillo     | Prioridad media |
| 🟢 Verde        | Prioridad baja o completado |

- **Clic en un nodo** del árbol → lo selecciona y abre su detalle.
- El árbol se actualiza automáticamente al crear, editar o eliminar nodos.

---

## 📊 Dashboard

La pestaña **📊 Dashboard** muestra tres gráficas:

1. **Gráfica circular** — Distribución completadas vs pendientes.
2. **Barras por prioridad** — Cuántas tareas hay en cada nivel.
3. **Diagrama de Gantt** — Los próximos 10 nodos con fecha, coloreados por urgencia:
   - 🔴 Rojo = ya venció
   - 🟡 Amarillo = vence en ≤ 3 días
   - 🟢 Verde/Teal = tiempo suficiente

---

## ⏱️ Pomodoro Timer

En la parte inferior del panel izquierdo encontrarás el temporizador Pomodoro:

- **▶** — Inicia / pausa el temporizador.
- **↺** — Reinicia a 25 minutos.
- Alterna automáticamente entre **TRABAJO (25 min)** y **DESCANSO (5 min)**.
- Al terminar cada ciclo envía una notificación del sistema operativo.

---

## 📤 Exportación

### Exportar PDF

1. Haz clic en **📤 Exportar PDF** (barra superior).
2. Elige dónde guardar el archivo.
3. El PDF incluye: resumen general, estadísticas y el árbol completo con jerarquía.

### Exportar Excel

1. Haz clic en **📊 Exportar Excel**.
2. El archivo `.xlsx` incluye todas las tareas en una tabla con colores por prioridad y estado.

### Importar desde CSV

1. Haz clic en **📥 Importar CSV**.
2. Selecciona tu archivo CSV (ver formato abajo).
3. Las tareas se agregan como nodos raíz.

**Formato CSV esperado:**
```csv
title,type,priority,due_date,tags,notes,status
Mi tarea,tarea,alta,2026-05-25,tag1;tag2,Notas aquí,pendiente
```

> Hay un archivo de ejemplo en `sample_import.csv` para probar.

---

## 💾 Persistencia de Datos

Los datos se guardan automáticamente en `data/arboris_data.json` cada vez que:
- Creas, editas o eliminas un nodo.
- Importas desde CSV.
- Cierras la aplicación.

Al abrir ARBORIS, carga automáticamente los datos del archivo.

---

## 🔔 Notificaciones del Sistema

Al iniciar la app, ARBORIS revisa todas las tareas y envía notificaciones nativas del OS si:
- Hay tareas **vencidas** (fecha pasada y no completadas).
- Hay tareas que **vencen hoy**.

---

## 📁 Estructura del Proyecto

```
arboris/
├── main.py                  ← Punto de entrada
├── requirements.txt         ← Dependencias
├── .env.example             ← Plantilla de configuración
├── sample_import.csv        ← CSV de ejemplo para importar
│
├── core/
│   ├── tree.py              ← Árbol n-ario (Node + ArborisTree)
│   ├── ai_module.py         ← Integración con Claude API
│   ├── exports.py           ← PDF, Excel, CSV
│   └── notifications.py     ← Alertas del sistema
│
├── gui/
│   └── app.py               ← Interfaz gráfica completa
│
└── data/                    ← Generado automáticamente
    └── arboris_data.json    ← Datos persistentes
```

---

## 🛠️ Solución de Problemas

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Ejecuta `pip install -r requirements.txt` |
| La IA no funciona | Verifica que `.env` existe y tiene tu API key real |
| El árbol no se dibuja | Instala `graphviz` del sistema: `sudo apt install graphviz` (Linux) o descárgalo en [graphviz.org](https://graphviz.org) |
| Sin notificaciones en macOS | Da permisos a Python en Configuración → Notificaciones |
| Error al exportar PDF | Verifica que tienes permisos de escritura en la carpeta destino |

---

## 📦 Dependencias

| Librería | Uso |
|----------|-----|
| `customtkinter` | GUI moderna con dark mode |
| `matplotlib` | Árbol visual + gráficas del dashboard |
| `networkx` | Lógica del grafo del árbol |
| `anthropic` | Claude API para funciones IA |
| `fpdf2` | Generación de reportes PDF |
| `openpyxl` | Exportación a Excel |
| `python-dotenv` | Carga de variables de entorno |
| `plyer` | Notificaciones del sistema operativo |

---

## 👨‍💻 Créditos

**ARBORIS** — Proyecto académico de Estructuras de Datos  
Desarrollado con Python 3.11+ · Mayo 2026

---

*"No entregues código. Entrega un producto."*
