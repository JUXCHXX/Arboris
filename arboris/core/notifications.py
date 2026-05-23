"""
ARBORIS - Notifications Module
Alertas del sistema para tareas vencidas
"""
from datetime import datetime, date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .tree import ArborisTree, Node


def check_and_notify(tree: "ArborisTree"):
    """Verifica tareas vencidas o que vencen hoy y lanza notificaciones del OS"""
    today = date.today()
    overdue = []
    due_today = []

    for node in tree.all_nodes():
        if node.status == "completado" or not node.due_date:
            continue
        try:
            d = datetime.strptime(node.due_date, "%Y-%m-%d").date()
            if d < today:
                overdue.append(node)
            elif d == today:
                due_today.append(node)
        except ValueError:
            continue

    try:
        from plyer import notification

        if overdue:
            titles = ", ".join(n.title[:20] for n in overdue[:3])
            notification.notify(
                title=f"⚠️ ARBORIS — {len(overdue)} tarea(s) vencida(s)",
                message=titles + ("..." if len(overdue) > 3 else ""),
                app_name="ARBORIS",
                timeout=8,
            )

        if due_today:
            titles = ", ".join(n.title[:20] for n in due_today[:3])
            notification.notify(
                title=f"📅 ARBORIS — {len(due_today)} tarea(s) vencen HOY",
                message=titles + ("..." if len(due_today) > 3 else ""),
                app_name="ARBORIS",
                timeout=8,
            )
    except Exception:
        pass  # plyer no disponible en todos los sistemas

    return overdue, due_today
