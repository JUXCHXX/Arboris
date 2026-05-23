"""
ARBORIS - Core Tree Structure
Árbol n-ario para gestión de tareas y proyectos
"""
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any


class Node:
    """Nodo del árbol — puede ser tarea o proyecto"""

    PRIORITIES = {"alta": 3, "media": 2, "baja": 1}
    TYPES = ["proyecto", "tarea", "subtarea", "nota"]
    STATUSES = ["pendiente", "en progreso", "completado", "cancelado"]

    def __init__(
        self,
        title: str,
        node_type: str = "tarea",
        priority: str = "media",
        due_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: str = "",
        status: str = "pendiente",
        node_id: Optional[str] = None,
    ):
        self.id = node_id or str(uuid.uuid4())[:8]
        self.title = title
        self.node_type = node_type
        self.priority = priority
        self.due_date = due_date  # "YYYY-MM-DD"
        self.tags = tags or []
        self.notes = notes
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.children: List["Node"] = []
        self.parent: Optional["Node"] = None

    # ── helpers ──────────────────────────────────────────────────────────────
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        try:
            return datetime.strptime(self.due_date, "%Y-%m-%d").date() < datetime.today().date()
        except ValueError:
            return False

    def priority_value(self) -> int:
        return self.PRIORITIES.get(self.priority, 1)

    def add_child(self, child: "Node"):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child_id: str) -> bool:
        for i, child in enumerate(self.children):
            if child.id == child_id:
                self.children.pop(i)
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "node_type": self.node_type,
            "priority": self.priority,
            "due_date": self.due_date,
            "tags": self.tags,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at,
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        node = cls(
            title=data["title"],
            node_type=data.get("node_type", "tarea"),
            priority=data.get("priority", "media"),
            due_date=data.get("due_date"),
            tags=data.get("tags", []),
            notes=data.get("notes", ""),
            status=data.get("status", "pendiente"),
            node_id=data.get("id"),
        )
        node.created_at = data.get("created_at", node.created_at)
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data)
            node.add_child(child)
        return node

    def __repr__(self):
        return f"Node({self.title!r}, {self.node_type}, {self.priority})"


class ArborisTree:
    """Árbol n-ario principal — contiene múltiples proyectos raíz"""

    def __init__(self):
        self.roots: List[Node] = []

    # ── CRUD ─────────────────────────────────────────────────────────────────
    def add_root(self, node: Node):
        self.roots.append(node)

    def find_node(self, node_id: str) -> Optional[Node]:
        def _search(n: Node) -> Optional[Node]:
            if n.id == node_id:
                return n
            for child in n.children:
                result = _search(child)
                if result:
                    return result
            return None

        for root in self.roots:
            result = _search(root)
            if result:
                return result
        return None

    def delete_node(self, node_id: str) -> bool:
        # check if it's a root
        for i, root in enumerate(self.roots):
            if root.id == node_id:
                self.roots.pop(i)
                return True

        # search parent and remove
        node = self.find_node(node_id)
        if node and node.parent:
            return node.parent.remove_child(node_id)
        return False

    def add_child_to(self, parent_id: str, child: Node) -> bool:
        parent = self.find_node(parent_id)
        if parent:
            parent.add_child(child)
            return True
        return False

    def search(
        self,
        query: str = "",
        priority: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        overdue_only: bool = False,
    ) -> List[Node]:
        results = []

        def _check(n: Node):
            match = True
            if query and query.lower() not in n.title.lower() and query.lower() not in n.notes.lower():
                match = False
            if priority and n.priority != priority:
                match = False
            if status and n.status != status:
                match = False
            if tag and tag not in n.tags:
                match = False
            if overdue_only and not n.is_overdue():
                match = False
            if match:
                results.append(n)
            for child in n.children:
                _check(child)

        for root in self.roots:
            _check(root)
        return results

    def all_nodes(self) -> List[Node]:
        return self.search()

    # ── stats ─────────────────────────────────────────────────────────────────
    def stats(self) -> Dict[str, Any]:
        all_n = self.all_nodes()
        total = len(all_n)
        completed = sum(1 for n in all_n if n.status == "completado")
        overdue = sum(1 for n in all_n if n.is_overdue() and n.status != "completado")
        by_priority = {p: sum(1 for n in all_n if n.priority == p) for p in ["alta", "media", "baja"]}
        by_type = {t: sum(1 for n in all_n if n.node_type == t) for t in Node.TYPES}
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "overdue": overdue,
            "completion_rate": round(completed / total * 100, 1) if total else 0,
            "by_priority": by_priority,
            "by_type": by_type,
        }

    # ── persistence ───────────────────────────────────────────────────────────
    def save(self, path: str = "data/arboris_data.json"):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.roots], f, ensure_ascii=False, indent=2)

    def load(self, path: str = "data/arboris_data.json"):
        import os
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.roots = [Node.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            self.roots = []
