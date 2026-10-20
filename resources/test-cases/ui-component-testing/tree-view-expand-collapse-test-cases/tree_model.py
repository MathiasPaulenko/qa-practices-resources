"""Modelo ejecutable de la lógica de una vista de árbol.

Implementa el comportamiento que ejercitan los casos de prueba de
QAPractices (TC001-TC024): expansión/colapso con persistencia de estado,
lazy loading de hijos con estados de error, selección, cascade de
checkboxes con indeterminate, type-ahead y drag-and-drop con
validación de referencias circulares.

Stdlib only — no browser required.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional


class CircularDropError(ValueError):
    """Raised when a node is dropped onto itself or a descendant."""


@dataclass
class Node:
    id: str
    label: str
    children: list["Node"] = field(default_factory=list)
    parent: Optional["Node"] = field(default=None, repr=False)
    expanded: bool = False
    selected: bool = False
    checked: bool = False
    lazy: bool = False           # children fetched on first expand
    loaded: bool = False         # lazy children already fetched
    load_error: bool = False     # last fetch failed

    def add_child(self, child: "Node") -> None:
        child.parent = self
        self.children.append(child)


class TreeModel:
    def __init__(self, roots: list[Node], fetcher: Optional[Callable[[Node], list[Node]]] = None):
        self.roots = roots
        self.fetcher = fetcher or (lambda node: [])
        self.focus: Optional[Node] = None

    # ---- lookup ------------------------------------------------------

    def find(self, label: str) -> Optional[Node]:
        stack = list(self.roots)
        while stack:
            node = stack.pop()
            if node.label == label:
                return node
            stack.extend(node.children)
        return None

    def visible_nodes(self) -> list[Node]:
        """Nodes reachable through expanded ancestors (render order)."""
        out: list[Node] = []
        def walk(nodes: list[Node]) -> None:
            for n in nodes:
                out.append(n)
                if n.expanded:
                    walk(n.children)
        walk(self.roots)
        return out

    # ---- expansion ---------------------------------------------------

    def expand(self, node: Node) -> list[Node]:
        node.expanded = True
        if node.lazy and not node.loaded and not node.load_error:
            try:
                node.children = self.fetcher(node)
                for c in node.children:
                    c.parent = node
                node.loaded = True
            except Exception:
                node.expanded = False
                node.load_error = True
        return node.children

    def collapse(self, node: Node) -> None:
        node.expanded = False

    def retry_load(self, node: Node) -> list[Node]:
        node.load_error = False
        return self.expand(node)

    def snapshot_expansion(self) -> set[str]:
        return {n.id for n in self._all() if n.expanded}

    def restore_expansion(self, ids: set[str]) -> None:
        for n in self._all():
            n.expanded = n.id in ids

    # ---- selection / keyboard ----------------------------------------

    def select(self, node: Node) -> None:
        for n in self._all():
            n.selected = n is node

    def move_focus(self, key: str) -> Optional[Node]:
        vis = self.visible_nodes()
        if not vis:
            return None
        if self.focus not in vis:
            self.focus = vis[0]
            return self.focus
        i = vis.index(self.focus)
        if key == "Home":
            self.focus = vis[0]
        elif key == "End":
            self.focus = vis[-1]
        elif key == "ArrowDown" and i < len(vis) - 1:
            self.focus = vis[i + 1]
        elif key == "ArrowUp" and i > 0:
            self.focus = vis[i - 1]
        elif key == "ArrowRight" and not self.focus.expanded:
            self.expand(self.focus)
        elif key == "ArrowLeft" and self.focus.expanded:
            self.collapse(self.focus)
        return self.focus

    def type_ahead(self, letter: str) -> Optional[Node]:
        """Focus the first visible node whose label starts with the letter."""
        letter = letter.lower()
        for n in self.visible_nodes():
            if n.label.lower().startswith(letter):
                self.focus = n
                return n
        return None

    # ---- checkboxes --------------------------------------------------

    def set_checked(self, node: Node, value: bool) -> None:
        node.checked = value
        for c in node.children:
            self.set_checked(c, value)
        self._update_ancestors(node.parent)

    def check_state(self, node: Node) -> str:
        """checked | unchecked | indeterminate."""
        if not node.children:
            return "checked" if node.checked else "unchecked"
        states = [self.check_state(c) for c in node.children]
        if all(s == "checked" for s in states) and node.checked:
            return "checked"
        if all(s == "unchecked" for s in states) and not node.checked:
            return "unchecked"
        return "indeterminate"

    def _update_ancestors(self, node: Optional[Node]) -> None:
        while node is not None:
            node.checked = all(c.checked for c in node.children)
            node = node.parent

    # ---- drag and drop -----------------------------------------------

    def move(self, node: Node, target: Node) -> None:
        if node is target or self._is_ancestor(node, target):
            raise CircularDropError("cannot drop a node onto itself or a descendant")
        if node.parent is not None:
            node.parent.children.remove(node)
        target.add_child(node)

    @staticmethod
    def _is_ancestor(ancestor: Node, node: Node) -> bool:
        cur = node.parent
        while cur is not None:
            if cur is ancestor:
                return True
            cur = cur.parent
        return False

    # ---- search ------------------------------------------------------

    def filter(self, query: str) -> list[Node]:
        """Visible subset: matching nodes plus their ancestors."""
        query = query.lower()
        keep: set[int] = set()
        for n in self._all():
            if query in n.label.lower():
                cur: Optional[Node] = n
                while cur is not None:
                    keep.add(id(cur))
                    cur = cur.parent
        return [n for n in self._all() if id(n) in keep]

    # ---- internal ----------------------------------------------------

    def _all(self) -> list[Node]:
        out: list[Node] = []
        stack = list(self.roots)
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(n.children)
        return out


def load_fixture(path: str | Path) -> TreeModel:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    def build(d: dict) -> Node:
        node = Node(id=d["id"], label=d["label"], lazy=d.get("lazy", False))
        for c in d.get("children", []):
            node.add_child(build(c))
        return node
    return TreeModel([build(d) for d in data])
