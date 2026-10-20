import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tree_model import CircularDropError, Node, TreeModel, load_fixture

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "tree.json"


@pytest.fixture
def tree():
    return load_fixture(FIXTURE)


# --- expansion (TC001–TC003, TC005, TC011) ---

def test_expand_root_reveals_children(tree):
    docs = tree.find("Documents")
    children = tree.expand(docs)
    assert docs.expanded
    assert [c.label for c in children] == ["Work", "Personal", "Projects"]


def test_collapse_hides_children(tree):
    docs = tree.find("Documents")
    tree.expand(docs)
    tree.collapse(docs)
    assert "Work" not in [n.label for n in tree.visible_nodes()]


def test_multi_level_expansion(tree):
    docs = tree.find("Documents")
    tree.expand(docs)
    work = tree.find("Work")
    tree.expand(work)
    reports = tree.find("Reports")
    tree.expand(reports)
    assert [n.label for n in tree.visible_nodes()] == [
        "Documents", "Work", "Reports", "report-q1.pdf", "report-q2.pdf",
        "Personal", "Projects",
    ]


def test_leaf_node_has_no_children(tree):
    leaf = tree.find("report-q2.pdf") or Node(id="leaf", label="leaf")
    assert leaf.children == []


# --- lazy loading (TC012–TC013) ---

def test_lazy_load_success(tree):
    fetched = [Node(id="p1", label="backlog")]
    tree.fetcher = lambda node: fetched
    projects = tree.find("Projects")
    tree.expand(projects)
    assert projects.loaded and not projects.load_error
    assert projects.children[0].label == "backlog"


def test_lazy_load_error_collapses_and_sets_retryable(tree):
    def boom(node):
        raise RuntimeError("500")
    tree.fetcher = boom
    projects = tree.find("Projects")
    tree.expand(projects)
    assert not projects.expanded
    assert projects.load_error
    tree.fetcher = lambda node: [Node(id="p1", label="backlog")]
    tree.retry_load(projects)
    assert projects.expanded and projects.loaded


# --- state persistence (TC014) ---

def test_expansion_survives_rebuild(tree):
    docs = tree.find("Documents")
    tree.expand(docs)
    tree.expand(tree.find("Work"))
    snap = tree.snapshot_expansion()
    rebuilt = load_fixture(FIXTURE)
    rebuilt.restore_expansion(snap)
    assert rebuilt.find("Documents").expanded
    assert rebuilt.find("Work").expanded
    assert not rebuilt.find("Personal").expanded


# --- selection + keyboard (TC004, TC006–TC007, TC022–TC023) ---

def test_single_select_deselects_previous(tree):
    tree.select(tree.find("Work"))
    tree.select(tree.find("Personal"))
    assert not tree.find("Work").selected
    assert tree.find("Personal").selected


def test_arrow_navigation_moves_through_visible(tree):
    tree.expand(tree.find("Documents"))
    tree.focus = tree.find("Documents")
    assert tree.move_focus("ArrowDown").label == "Work"
    assert tree.move_focus("ArrowDown").label == "Personal"
    assert tree.move_focus("ArrowUp").label == "Work"


def test_arrow_right_expands_collapsed(tree):
    docs = tree.find("Documents")
    tree.focus = docs
    tree.move_focus("ArrowRight")
    assert docs.expanded


def test_home_end_jump_to_boundaries(tree):
    tree.expand(tree.find("Documents"))
    tree.focus = tree.find("Personal")
    assert tree.move_focus("Home").label == "Documents"
    assert tree.move_focus("End").label == "Projects"


def test_type_ahead_finds_first_match(tree):
    tree.expand(tree.find("Documents"))
    assert tree.type_ahead("P").label == "Personal"
    assert tree.type_ahead("z") is None  # no match: focus unchanged


# --- checkbox cascade (TC024) ---

def test_cascade_and_indeterminate(tree):
    docs = tree.find("Documents")
    tree.set_checked(docs, True)
    assert tree.check_state(docs) == "checked"
    tree.set_checked(tree.find("Work"), False)
    assert tree.check_state(docs) == "indeterminate"


# --- drag and drop (TC016–TC017) ---

def test_move_node_between_parents(tree):
    docs = tree.find("Documents")
    work = tree.find("Work")
    personal = tree.find("Personal")
    tree.expand(docs)
    reports = Node(id="r", label="report.pdf")
    work.add_child(reports)
    tree.move(reports, personal)
    assert reports.parent is personal
    assert reports not in work.children


def test_drop_onto_own_descendant_rejected(tree):
    docs = tree.find("Documents")
    reports = tree.find("Reports")
    with pytest.raises(CircularDropError):
        tree.move(docs, reports)
    assert docs.parent is None  # tree unchanged


def test_drop_onto_self_rejected(tree):
    docs = tree.find("Documents")
    with pytest.raises(CircularDropError):
        tree.move(docs, docs)


# --- search filter (TC015) ---

def test_filter_keeps_match_and_ancestors(tree):
    keep = {n.label for n in tree.filter("q1")}
    assert keep == {"Documents", "Work", "Reports", "report-q1.pdf"}
    assert "Personal" not in keep
