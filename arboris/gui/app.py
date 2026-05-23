"""
ARBORIS - Main GUI Application
Interface principal con CustomTkinter
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from datetime import datetime, date
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
ENV_EXAMPLE_PATH = os.path.join(BASE_DIR, ".env.example")

# load .env
try:
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH)
    if not os.getenv("GROQ_API_KEY"):
        load_dotenv(ENV_EXAMPLE_PATH)
except ImportError:
    pass

from core import (
    Node, ArborisTree,
    suggest_task_attributes, generate_project_summary, detect_duplicates,
    export_pdf, export_excel, import_from_csv,
    check_and_notify,
)

# ── THEME ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLORS = {
    "bg":      "#0D0F14",
    "surface": "#141720",
    "card":    "#1C2030",
    "accent":  "#00E5BE",
    "accent2": "#7B61FF",
    "muted":   "#8892A4",
    "white":   "#F0F4FF",
    "warn":    "#FF6B6B",
    "gold":    "#FFD166",
    "success": "#06D6A0",
    "selected": "#332B57",
}

PRIORITY_COLORS = {"alta": COLORS["warn"], "media": COLORS["gold"], "baja": COLORS["success"]}
STATUS_ICONS = {"pendiente": "○", "en progreso": "►", "completado": "✓", "cancelado": "✗"}

DATA_PATH = os.path.join(BASE_DIR, "data", "arboris_data.json")


# ═══════════════════════════════════════════════════════════════════════════════
class NodeDialog(ctk.CTkToplevel):
    """Diálogo para crear/editar un nodo"""

    def __init__(self, master, title="Nueva Tarea", node: Node = None, ai_desc=""):
        super().__init__(master)
        self.title(title)
        self.geometry("540x600")
        self.configure(fg_color=COLORS["surface"])
        self.resizable(False, False)
        self.grab_set()
        self.result: Node = None

        self._build(node, ai_desc)

    def _build(self, node, ai_desc):
        # header
        ctk.CTkLabel(self, text=self.title(), font=("Helvetica", 18, "bold"),
                      text_color=COLORS["accent"]).pack(pady=(20, 5))

        form = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        def field(label, widget_fn, **kw):
            ctk.CTkLabel(form, text=label, font=("Helvetica", 11),
                          text_color=COLORS["muted"], anchor="w").pack(fill="x", padx=16, pady=(10, 2))
            w = widget_fn(form, **kw)
            w.pack(fill="x", padx=16, pady=(0, 4))
            return w

        # Title
        self.title_var = tk.StringVar(value=node.title if node else ai_desc[:60])
        self.title_entry = field("Título *", ctk.CTkEntry,
                                  textvariable=self.title_var,
                                  placeholder_text="Ej: Diseñar interfaz principal",
                                  font=("Helvetica", 12))

        # Type & Priority side by side
        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(row, text="Tipo", text_color=COLORS["muted"], font=("Helvetica", 11)).pack(side="left", padx=(0, 8))
        self.type_var = tk.StringVar(value=node.node_type if node else "tarea")
        ctk.CTkOptionMenu(row, variable=self.type_var,
                           values=Node.TYPES,
                           fg_color=COLORS["bg"],
                           button_color=COLORS["accent2"],
                           width=130).pack(side="left")

        ctk.CTkLabel(row, text="Prioridad", text_color=COLORS["muted"], font=("Helvetica", 11)).pack(side="left", padx=(20, 8))
        self.priority_var = tk.StringVar(value=node.priority if node else "media")
        ctk.CTkOptionMenu(row, variable=self.priority_var,
                           values=["alta", "media", "baja"],
                           fg_color=COLORS["bg"],
                           button_color=COLORS["accent2"],
                           width=110).pack(side="left")

        # Status
        ctk.CTkLabel(form, text="Estado", text_color=COLORS["muted"], font=("Helvetica", 11), anchor="w").pack(fill="x", padx=16, pady=(6, 2))
        self.status_var = tk.StringVar(value=node.status if node else "pendiente")
        ctk.CTkOptionMenu(form, variable=self.status_var,
                           values=Node.STATUSES,
                           fg_color=COLORS["bg"],
                           button_color=COLORS["accent2"]).pack(fill="x", padx=16)

        # Due date
        self.due_var = tk.StringVar(value=node.due_date if node and node.due_date else "")
        field("Fecha de vencimiento (YYYY-MM-DD)", ctk.CTkEntry,
              textvariable=self.due_var, placeholder_text="2026-05-23")

        # Tags
        self.tags_var = tk.StringVar(value=", ".join(node.tags) if node else "")
        field("Etiquetas (separadas por coma)", ctk.CTkEntry,
              textvariable=self.tags_var, placeholder_text="diseño, backend, urgente")

        # Notes
        ctk.CTkLabel(form, text="Notas", font=("Helvetica", 11),
                      text_color=COLORS["muted"], anchor="w").pack(fill="x", padx=16, pady=(10, 2))
        self.notes_box = ctk.CTkTextbox(form, height=80, fg_color=COLORS["bg"],
                                         font=("Helvetica", 11))
        self.notes_box.pack(fill="x", padx=16, pady=(0, 12))
        if node and node.notes:
            self.notes_box.insert("1.0", node.notes)

        # buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=10)
        ctk.CTkButton(btn_row, text="Cancelar", width=120,
                       fg_color=COLORS["card"], hover_color=COLORS["bg"],
                       command=self.destroy).pack(side="left", padx=6)
        ctk.CTkButton(btn_row, text="✓  Guardar", width=150,
                       fg_color=COLORS["accent"], text_color=COLORS["bg"],
                       hover_color="#00c9a7",
                       font=("Helvetica", 13, "bold"),
                       command=self._save).pack(side="left", padx=6)

    def _save(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "El título es obligatorio.", parent=self)
            return

        due = self.due_var.get().strip() or None
        if due:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD", parent=self)
                return

        tags = [t.strip() for t in self.tags_var.get().split(",") if t.strip()]
        notes = self.notes_box.get("1.0", "end").strip()

        self.result = Node(
            title=title,
            node_type=self.type_var.get(),
            priority=self.priority_var.get(),
            due_date=due,
            tags=tags,
            notes=notes,
            status=self.status_var.get(),
        )
        self.destroy()


# ═══════════════════════════════════════════════════════════════════════════════
class PomodoroWidget(ctk.CTkFrame):
    """Widget Pomodoro integrado"""

    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["card"], corner_radius=12)
        self.work_mins = 25
        self.break_mins = 5
        self.remaining = self.work_mins * 60
        self.running = False
        self.on_break = False
        self._job = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="⏱  POMODORO", font=("Helvetica", 11, "bold"),
                      text_color=COLORS["accent"]).pack(pady=(12, 4))

        self.mode_label = ctk.CTkLabel(self, text="TRABAJO", font=("Helvetica", 9),
                                        text_color=COLORS["muted"])
        self.mode_label.pack()

        self.timer_label = ctk.CTkLabel(self, text="25:00", font=("Helvetica", 32, "bold"),
                                         text_color=COLORS["white"])
        self.timer_label.pack(pady=6)

        self.progress = ctk.CTkProgressBar(self, width=180, progress_color=COLORS["accent"])
        self.progress.set(1.0)
        self.progress.pack(pady=4)

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(4, 12))

        self.start_btn = ctk.CTkButton(btn_row, text="▶", width=50,
                                        fg_color=COLORS["accent"], text_color=COLORS["bg"],
                                        font=("Helvetica", 14, "bold"),
                                        command=self.toggle)
        self.start_btn.pack(side="left", padx=4)

        ctk.CTkButton(btn_row, text="↺", width=50,
                       fg_color=COLORS["card"], hover_color=COLORS["bg"],
                       font=("Helvetica", 14),
                       command=self.reset).pack(side="left", padx=4)

    def toggle(self):
        self.running = not self.running
        self.start_btn.configure(text="⏸" if self.running else "▶")
        if self.running:
            self._tick()

    def _tick(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self.running = False
            self.on_break = not self.on_break
            self.remaining = (self.break_mins if self.on_break else self.work_mins) * 60
            mode = "DESCANSO" if self.on_break else "TRABAJO"
            self.mode_label.configure(text=mode)
            try:
                from plyer import notification
                notification.notify(title="ARBORIS Pomodoro",
                                    message=f"¡Tiempo! Cambio a {mode}", timeout=5)
            except Exception:
                pass
        mins, secs = divmod(self.remaining, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        total = (self.break_mins if self.on_break else self.work_mins) * 60
        self.progress.set(self.remaining / total)
        self.remaining -= 1
        self._job = self.after(1000, self._tick)

    def reset(self):
        self.running = False
        self.on_break = False
        self.remaining = self.work_mins * 60
        self.timer_label.configure(text="25:00")
        self.progress.set(1.0)
        self.start_btn.configure(text="▶")
        self.mode_label.configure(text="TRABAJO")


# ═══════════════════════════════════════════════════════════════════════════════
class TreeView(ctk.CTkFrame):
    """Panel de visualización del árbol con matplotlib"""

    def __init__(self, master, tree: ArborisTree, on_select=None):
        super().__init__(master, fg_color=COLORS["bg"])
        self.tree = tree
        self.on_select = on_select
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor(COLORS["bg"])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.mpl_connect("button_press_event", self._on_click)
        self._node_positions = {}
        self.refresh()

    def refresh(self):
        self.ax.clear()
        self.ax.set_facecolor(COLORS["bg"])
        self._node_positions.clear()

        if not self.tree.roots:
            self.ax.text(0.5, 0.5, "No hay proyectos aún\n\nUsa el panel izquierdo\npara crear uno",
                         ha="center", va="center", color=COLORS["muted"],
                         fontsize=13, transform=self.ax.transAxes)
            self.ax.axis("off")
            self.canvas.draw()
            return

        G = nx.DiGraph()
        node_colors = {}
        node_labels = {}
        edge_list = []

        def add_nodes(n, parent_id=None):
            G.add_node(n.id)
            short = n.title[:18] + "…" if len(n.title) > 18 else n.title
            icon = {"proyecto": "[P]", "tarea": "[T]", "subtarea": ">", "nota": "[N]"}.get(n.node_type, "")
            node_labels[n.id] = f"{icon} {short}"
            if n.is_overdue() and n.status != "completado":
                node_colors[n.id] = COLORS["warn"]
            elif n.status == "completado":
                node_colors[n.id] = COLORS["success"]
            else:
                node_colors[n.id] = PRIORITY_COLORS.get(n.priority, COLORS["muted"])
            if parent_id:
                G.add_edge(parent_id, n.id)
                edge_list.append((parent_id, n.id))
            for child in n.children:
                add_nodes(child, n.id)

        for root in self.tree.roots:
            add_nodes(root)

        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        except Exception:
            try:
                pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
            except Exception:
                pos = nx.spring_layout(G, k=2, seed=42)

        self._node_positions = pos

        colors_list = [node_colors.get(n, COLORS["muted"]) for n in G.nodes()]

        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color=COLORS["muted"],
                               arrows=True, arrowsize=15, width=1.2,
                               connectionstyle="arc3,rad=0.1")
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=colors_list,
                               node_size=1600, alpha=0.92)
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=self.ax,
                                font_size=7, font_color=COLORS["bg"],
                                font_weight="bold")

        # legend
        legend_items = [
            mpatches.Patch(color=COLORS["warn"], label="Alta / Vencido"),
            mpatches.Patch(color=COLORS["gold"], label="Media"),
            mpatches.Patch(color=COLORS["success"], label="Baja / Completado"),
        ]
        self.ax.legend(handles=legend_items, loc="lower right",
                        facecolor=COLORS["card"], edgecolor=COLORS["muted"],
                        labelcolor=COLORS["white"], fontsize=8)

        self.ax.axis("off")
        self.canvas.draw()

    def _on_click(self, event):
        if not event.xdata or not event.ydata or not self.on_select:
            return
        closest = None
        min_dist = float("inf")
        for node_id, (px, py) in self._node_positions.items():
            dist = ((event.xdata - px) ** 2 + (event.ydata - py) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest = node_id
        if closest and min_dist < 30:
            self.on_select(closest)


# ═══════════════════════════════════════════════════════════════════════════════
class DashboardView(ctk.CTkFrame):
    """Vista de estadísticas y Gantt"""

    def __init__(self, master, tree: ArborisTree):
        super().__init__(master, fg_color=COLORS["bg"])
        self.tree = tree
        self._build()

    def _build(self):
        self.fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        self.fig.patch.set_facecolor(COLORS["bg"])
        self.ax_pie, self.ax_bar, self.ax_gantt = axes
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for ax in [self.ax_pie, self.ax_bar, self.ax_gantt]:
            ax.clear()
            ax.set_facecolor(COLORS["surface"])

        stats = self.tree.stats()

        # ── pie: status ───────────────────────────────────────────────────────
        completed = stats["completed"]
        pending = stats["pending"]
        if completed + pending > 0:
            self.ax_pie.pie(
                [completed, pending],
                labels=["Completadas", "Pendientes"],
                colors=[COLORS["success"], COLORS["accent2"]],
                autopct="%1.0f%%",
                textprops={"color": COLORS["white"], "fontsize": 9},
                startangle=90,
            )
        self.ax_pie.set_title("Estado", color=COLORS["accent"], fontsize=11, pad=10)

        # ── bar: priority ─────────────────────────────────────────────────────
        bp = stats["by_priority"]
        bars = self.ax_bar.bar(
            ["Alta", "Media", "Baja"],
            [bp["alta"], bp["media"], bp["baja"]],
            color=[COLORS["warn"], COLORS["gold"], COLORS["success"]],
            width=0.5,
        )
        self.ax_bar.set_title("Por Prioridad", color=COLORS["accent"], fontsize=11, pad=10)
        self.ax_bar.tick_params(colors=COLORS["muted"])
        self.ax_bar.spines[:].set_color(COLORS["card"])
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                self.ax_bar.text(bar.get_x() + bar.get_width()/2, h + 0.05, str(int(h)),
                                  ha="center", color=COLORS["white"], fontsize=9)

        # ── gantt ─────────────────────────────────────────────────────────────
        nodes_with_dates = [n for n in self.tree.all_nodes() if n.due_date][:10]
        if nodes_with_dates:
            today = date.today()
            for i, node in enumerate(nodes_with_dates):
                try:
                    d = datetime.strptime(node.due_date, "%Y-%m-%d").date()
                    days_left = (d - today).days
                    color = COLORS["warn"] if days_left < 0 else (COLORS["gold"] if days_left <= 3 else COLORS["accent"])
                    self.ax_gantt.barh(i, max(days_left, 1), left=0,
                                       color=color, alpha=0.8, height=0.6)
                    short = node.title[:20] + "…" if len(node.title) > 20 else node.title
                    self.ax_gantt.text(-0.2, i, short, ha="right", va="center",
                                       color=COLORS["white"], fontsize=7)
                except ValueError:
                    continue
            self.ax_gantt.axvline(0, color=COLORS["white"], linewidth=1, alpha=0.5)
            self.ax_gantt.set_xlabel("Días hasta vencimiento", color=COLORS["muted"], fontsize=8)
            self.ax_gantt.tick_params(colors=COLORS["muted"], labelleft=False)
            self.ax_gantt.spines[:].set_color(COLORS["card"])
        else:
            self.ax_gantt.text(0.5, 0.5, "Sin fechas asignadas",
                               ha="center", va="center", color=COLORS["muted"], fontsize=10,
                               transform=self.ax_gantt.transAxes)
            self.ax_gantt.axis("off")

        self.ax_gantt.set_title("Gantt (próximos)", color=COLORS["accent"], fontsize=11, pad=10)
        self.fig.tight_layout(pad=2)
        self.canvas.draw()


# ═══════════════════════════════════════════════════════════════════════════════
class App(ctk.CTk):
    """Ventana principal de ARBORIS"""

    def __init__(self):
        super().__init__()
        self.title("ARBORIS — Gestión de Proyectos")
        self.geometry("1280x780")
        self.minsize(960, 640)
        self.configure(fg_color=COLORS["bg"])

        self.tree = ArborisTree()
        self.tree.load(DATA_PATH)
        self.selected_node_id = None

        self._build_ui()
        self._refresh_tree_list()

        # check notifications on start
        threading.Thread(target=check_and_notify, args=(self.tree,), daemon=True).start()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI BUILD ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── top bar ───────────────────────────────────────────────────────────
        topbar = ctk.CTkFrame(self, height=52, fg_color=COLORS["surface"], corner_radius=0)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="  🌳  ARBORIS", font=("Helvetica", 20, "bold"),
                      text_color=COLORS["accent"]).pack(side="left", padx=20)

        # search
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_tree_list())
        search = ctk.CTkEntry(topbar, textvariable=self.search_var, width=240,
                               placeholder_text="🔍  Buscar tareas...",
                               fg_color=COLORS["card"],
                               border_color=COLORS["accent2"])
        search.pack(side="left", padx=16, pady=10)

        # filter dropdowns
        self.filter_priority = tk.StringVar(value="todas")
        ctk.CTkOptionMenu(topbar, variable=self.filter_priority,
                           values=["todas", "alta", "media", "baja"],
                           width=120, fg_color=COLORS["card"],
                           button_color=COLORS["accent2"],
                           command=lambda _: self._refresh_tree_list()).pack(side="left", padx=4)

        self.filter_status = tk.StringVar(value="todos")
        ctk.CTkOptionMenu(topbar, variable=self.filter_status,
                           values=["todos"] + Node.STATUSES,
                           width=140, fg_color=COLORS["card"],
                           button_color=COLORS["accent2"],
                           command=lambda _: self._refresh_tree_list()).pack(side="left", padx=4)

        # top-right buttons
        for text, cmd, color in [
            ("📤 Exportar PDF", self._export_pdf, COLORS["accent2"]),
            ("📊 Exportar Excel", self._export_excel, COLORS["accent"]),
            ("📥 Importar CSV", self._import_csv, COLORS["card"]),
        ]:
            ctk.CTkButton(topbar, text=text, command=cmd,
                           fg_color=color, text_color=COLORS["white"] if color != COLORS["accent"] else COLORS["bg"],
                           width=140, height=32,
                           font=("Helvetica", 11)).pack(side="right", padx=6, pady=10)

        # ── main area ─────────────────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # left panel
        left = ctk.CTkFrame(main, width=280, fg_color=COLORS["surface"], corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # action buttons
        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.pack(fill="x", padx=12, pady=12)

        ctk.CTkButton(actions, text="＋  Nuevo Proyecto", width=120,
                       fg_color=COLORS["accent"], text_color=COLORS["bg"],
                       font=("Helvetica", 12, "bold"),
                       command=self._new_root_node).pack(side="left", padx=(0, 6))

        ctk.CTkButton(actions, text="➕  Subtarea", width=110,
                       fg_color=COLORS["accent2"],
                       font=("Helvetica", 12, "bold"),
                       command=self._new_child_node).pack(side="left")

        # AI input
        ai_frame = ctk.CTkFrame(left, fg_color=COLORS["card"], corner_radius=10)
        ai_frame.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(ai_frame, text="🤖  IA — Describe tu tarea",
                      font=("Helvetica", 10, "bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 4))
        self.ai_entry = ctk.CTkEntry(ai_frame, placeholder_text="Ej: reunión urgente con cliente mañana...",
                                      fg_color=COLORS["bg"])
        self.ai_entry.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkButton(ai_frame, text="✨ Sugerir con IA", height=30,
                       fg_color=COLORS["accent2"],
                       command=self._ai_suggest).pack(fill="x", padx=10, pady=(0, 10))

        # node list
        ctk.CTkLabel(left, text="PROYECTOS Y TAREAS", font=("Helvetica", 10, "bold"),
                      text_color=COLORS["muted"]).pack(anchor="w", padx=16, pady=(8, 4))

        self.node_list_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.node_list_frame.pack(fill="both", expand=True, padx=8)

        # pomodoro at bottom of left
        self.pomodoro = PomodoroWidget(left)
        self.pomodoro.pack(fill="x", padx=12, pady=12)

        # ── right panel with tabs ─────────────────────────────────────────────
        right = ctk.CTkFrame(main, fg_color=COLORS["bg"], corner_radius=0)
        right.pack(side="left", fill="both", expand=True)

        self.tabview = ctk.CTkTabview(right, fg_color=COLORS["surface"],
                                       segmented_button_selected_color=COLORS["accent"],
                                       segmented_button_selected_hover_color="#00c9a7",
                                       segmented_button_unselected_color=COLORS["card"],
                                       text_color=COLORS["white"])
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("🌳  Árbol")
        self.tabview.add("📊  Dashboard")
        self.tabview.add("📋  Detalle")

        # tree tab
        self.tree_view = TreeView(self.tabview.tab("🌳  Árbol"), self.tree,
                                   on_select=self._on_tree_node_click)
        self.tree_view.pack(fill="both", expand=True)

        # dashboard tab
        self.dashboard = DashboardView(self.tabview.tab("📊  Dashboard"), self.tree)
        self.dashboard.pack(fill="both", expand=True)

        # detail tab
        self._build_detail_panel()

        # status bar
        self.status_var = tk.StringVar(value="Listo — ARBORIS v1.0")
        status_bar = ctk.CTkLabel(self, textvariable=self.status_var,
                                   font=("Helvetica", 9), text_color=COLORS["muted"],
                                   anchor="w")
        status_bar.pack(fill="x", side="bottom", padx=16, pady=4)

    def _build_detail_panel(self):
        tab = self.tabview.tab("📋  Detalle")

        self.detail_title = ctk.CTkLabel(tab, text="Selecciona un nodo del árbol",
                                          font=("Helvetica", 20, "bold"),
                                          text_color=COLORS["accent"])
        self.detail_title.pack(pady=(20, 4))

        self.detail_meta = ctk.CTkLabel(tab, text="", font=("Helvetica", 11),
                                         text_color=COLORS["muted"])
        self.detail_meta.pack()

        self.detail_notes = ctk.CTkTextbox(tab, height=120, fg_color=COLORS["card"],
                                            state="disabled")
        self.detail_notes.pack(fill="x", padx=30, pady=12)

        btn_row = ctk.CTkFrame(tab, fg_color="transparent")
        btn_row.pack(pady=8)

        ctk.CTkButton(btn_row, text="✏️  Editar", width=140,
                       fg_color=COLORS["accent2"],
                       command=self._edit_selected).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="🗑  Eliminar", width=140,
                       fg_color=COLORS["warn"],
                       command=self._delete_selected).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="🤖  Resumen IA", width=160,
                       fg_color=COLORS["card"],
                       command=self._ai_summary).pack(side="left", padx=8)

        self.ai_summary_box = ctk.CTkTextbox(tab, height=200, fg_color=COLORS["card"],
                                              state="disabled", wrap="word")
        self.ai_summary_box.pack(fill="x", padx=30, pady=8)

    # ── node list ─────────────────────────────────────────────────────────────
    def _refresh_tree_list(self):
        for w in self.node_list_frame.winfo_children():
            w.destroy()

        query = self.search_var.get().strip()
        priority = self.filter_priority.get()
        status = self.filter_status.get()

        results = self.tree.search(
            query=query,
            priority=None if priority == "todas" else priority,
            status=None if status == "todos" else status,
        )

        if not results:
            ctk.CTkLabel(self.node_list_frame, text="Sin resultados",
                          text_color=COLORS["muted"], font=("Helvetica", 11)).pack(pady=20)
            return

        for node in results:
            self._node_card(node)

    def _node_card(self, node: Node):
        selected = node.id == self.selected_node_id
        col = PRIORITY_COLORS.get(node.priority, COLORS["muted"])
        bg = COLORS["selected"] if selected else COLORS["card"]

        card = ctk.CTkFrame(self.node_list_frame, fg_color=bg, corner_radius=8,
                             border_width=1 if selected else 0,
                             border_color=COLORS["accent2"])
        card.pack(fill="x", pady=3, padx=2)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(8, 2))

        icon = {"proyecto": "📁", "tarea": "✅", "subtarea": "▸", "nota": "📝"}.get(node.node_type, "")
        status_icon = STATUS_ICONS.get(node.status, "○")
        overdue = " 🔴" if node.is_overdue() and node.status != "completado" else ""

        ctk.CTkLabel(top, text=f"{status_icon}  {icon} {node.title[:28]}{overdue}",
                      font=("Helvetica", 11, "bold"),
                      text_color=col if not selected else COLORS["white"],
                      anchor="w").pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(card, text=f"  {node.priority.upper()} · {node.due_date or 'Sin fecha'} · {len(node.children)} hijos",
                      font=("Helvetica", 9), text_color=COLORS["white"] if selected else COLORS["muted"],
                      anchor="w").pack(fill="x", padx=10, pady=(0, 6))

        card.bind("<Button-1>", lambda e, nid=node.id: self._select_node(nid))
        for w in card.winfo_children():
            w.bind("<Button-1>", lambda e, nid=node.id: self._select_node(nid))
            for ww in w.winfo_children():
                ww.bind("<Button-1>", lambda e, nid=node.id: self._select_node(nid))

    # ── selection ─────────────────────────────────────────────────────────────
    def _select_node(self, node_id: str):
        self.selected_node_id = node_id
        self._refresh_tree_list()
        self._update_detail()
        self.tabview.set("📋  Detalle")

    def _on_tree_node_click(self, node_id: str):
        self._select_node(node_id)

    def _update_detail(self):
        node = self.tree.find_node(self.selected_node_id)
        if not node:
            return
        self.detail_title.configure(text=node.title)
        meta = f"{node.node_type.upper()} · {node.priority} · {node.status}"
        if node.due_date:
            meta += f" · Vence: {node.due_date}"
        if node.tags:
            meta += f"\n🏷  {', '.join(node.tags)}"
        self.detail_meta.configure(text=meta)
        self.detail_notes.configure(state="normal")
        self.detail_notes.delete("1.0", "end")
        self.detail_notes.insert("1.0", node.notes or "Sin notas.")
        self.detail_notes.configure(state="disabled")

        # clear AI box
        self.ai_summary_box.configure(state="normal")
        self.ai_summary_box.delete("1.0", "end")
        self.ai_summary_box.configure(state="disabled")

    # ── actions ───────────────────────────────────────────────────────────────
    def _new_root_node(self):
        dlg = NodeDialog(self, "Nuevo Proyecto / Tarea Raíz")
        self.wait_window(dlg)
        if dlg.result:
            self.tree.add_root(dlg.result)
            self._save_and_refresh()
            self.status_var.set(f"✅ Creado: {dlg.result.title}")

    def _new_child_node(self):
        if not self.selected_node_id:
            messagebox.showinfo("Info", "Selecciona primero un nodo padre.", parent=self)
            return
        dlg = NodeDialog(self, "Nueva Subtarea")
        self.wait_window(dlg)
        if dlg.result:
            self.tree.add_child_to(self.selected_node_id, dlg.result)
            self._save_and_refresh()
            self.status_var.set(f"✅ Subtarea creada: {dlg.result.title}")

    def _edit_selected(self):
        node = self.tree.find_node(self.selected_node_id)
        if not node:
            messagebox.showinfo("Info", "Selecciona un nodo primero.", parent=self)
            return
        dlg = NodeDialog(self, "Editar Nodo", node=node)
        self.wait_window(dlg)
        if dlg.result:
            dlg.result.id = node.id
            dlg.result.children = node.children
            dlg.result.parent = node.parent
            dlg.result.created_at = node.created_at
            if node.parent:
                for i, c in enumerate(node.parent.children):
                    if c.id == node.id:
                        node.parent.children[i] = dlg.result
                        break
            else:
                for i, r in enumerate(self.tree.roots):
                    if r.id == node.id:
                        self.tree.roots[i] = dlg.result
                        break
            self._save_and_refresh()
            self.selected_node_id = dlg.result.id
            self._update_detail()
            self.status_var.set(f"✏️ Editado: {dlg.result.title}")

    def _delete_selected(self):
        node = self.tree.find_node(self.selected_node_id)
        if not node:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{node.title}' y todos sus hijos?", parent=self):
            self.tree.delete_node(self.selected_node_id)
            self.selected_node_id = None
            self._save_and_refresh()
            self.status_var.set("🗑  Nodo eliminado.")

    # ── AI ────────────────────────────────────────────────────────────────────
    def _ai_suggest(self):
        desc = self.ai_entry.get().strip()
        if not desc:
            return
        self.status_var.set("🤖 Consultando IA...")
        self.update()

        def run():
            result = suggest_task_attributes(desc)
            self.after(0, lambda: self._open_ai_dialog(result, desc))

        threading.Thread(target=run, daemon=True).start()

    def _open_ai_dialog(self, result, original_desc):
        if "error" in result:
            self.status_var.set(f"⚠️ {result['error']}")

        # check duplicates
        existing = [n.title for n in self.tree.all_nodes()]
        dup = detect_duplicates(result.get("title", original_desc), existing)
        if dup:
            if not messagebox.askyesno("Posible duplicado",
                                        f"¿Ya existe una tarea similar: '{dup}'?\n¿Quieres crearla de todas formas?",
                                        parent=self):
                self.status_var.set("IA: Creación cancelada por duplicado.")
                return

        dlg = NodeDialog(self, "✨ Nueva Tarea (sugerida por IA)")
        # pre-fill
        dlg.title_var.set(result.get("title", original_desc)[:60])
        dlg.priority_var.set(result.get("priority", "media"))
        dlg.type_var.set(result.get("node_type", "tarea"))
        if result.get("due_date"):
            dlg.due_var.set(result["due_date"])
        if result.get("tags"):
            dlg.tags_var.set(", ".join(result["tags"]))
        if result.get("notes"):
            dlg.notes_box.insert("1.0", result["notes"])

        self.wait_window(dlg)
        if dlg.result:
            self.tree.add_root(dlg.result)
            self._save_and_refresh()
            self.ai_entry.delete(0, "end")
            self.status_var.set(f"✨ IA creó: {dlg.result.title}")

    def _ai_summary(self):
        node = self.tree.find_node(self.selected_node_id)
        if not node:
            return
        self.status_var.set("🤖 Generando resumen...")
        self.update()

        def run():
            summary = generate_project_summary(node.to_dict())
            self.after(0, lambda: self._show_summary(summary))

        threading.Thread(target=run, daemon=True).start()

    def _show_summary(self, text: str):
        self.ai_summary_box.configure(state="normal")
        self.ai_summary_box.delete("1.0", "end")
        self.ai_summary_box.insert("1.0", text)
        self.ai_summary_box.configure(state="disabled")
        if text.startswith("⚠") or text.startswith("Error"):
            self.status_var.set(text)
        else:
            self.status_var.set("✅ Resumen generado.")

    # ── exports ───────────────────────────────────────────────────────────────
    def _export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF", "*.pdf")],
                                             initialfile="arboris_report.pdf")
        if path:
            threading.Thread(target=lambda: self._do_export_pdf(path), daemon=True).start()

    def _do_export_pdf(self, path):
        try:
            export_pdf(self.tree, path)
            self.after(0, lambda: self.status_var.set(f"📤 PDF exportado: {path}"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e), parent=self))

    def _export_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel", "*.xlsx")],
                                             initialfile="arboris_report.xlsx")
        if path:
            threading.Thread(target=lambda: self._do_export_excel(path), daemon=True).start()

    def _do_export_excel(self, path):
        try:
            export_excel(self.tree, path)
            self.after(0, lambda: self.status_var.set(f"📊 Excel exportado: {path}"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e), parent=self))

    def _import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            count = import_from_csv(path, self.tree)
            self._save_and_refresh()
            self.status_var.set(f"📥 {count} tareas importadas desde CSV.")

    # ── utils ─────────────────────────────────────────────────────────────────
    def _save_and_refresh(self):
        self.tree.save(DATA_PATH)
        self.tree_view.refresh()
        self.dashboard.refresh()
        self._refresh_tree_list()

    def _on_close(self):
        self.tree.save(DATA_PATH)
        self.quit()
        self.destroy()


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
