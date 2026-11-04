"""Flag combination matrix test — exercises every 2^n state of a small flag set.

Run: pytest flag_matrix_test.py -v
"""
import itertools
import json
from pathlib import Path

import pytest

CONFIG = json.loads((Path(__file__).parent / "flag-config.json").read_text())
FLAGS = list(CONFIG.keys())


def resolve_flags(state: dict) -> str:
    """Minimal flag evaluator under test: dependencies then conflicts."""
    for flag, cfg in CONFIG.items():
        if state.get(flag) and cfg.get("enabled", True):
            for dep in cfg.get("dependencies", []):
                if not state.get(dep):
                    return "missing_dependency"
            for conflict in cfg.get("conflicts", []):
                if state.get(conflict):
                    return "conflict"
    return "ok"


@pytest.mark.parametrize(
    "combo",
    list(itertools.product([True, False], repeat=len(FLAGS))),
    ids=[str(c) for c in itertools.product([True, False], repeat=len(FLAGS))],
)
def test_flag_combinations(combo):
    state = dict(zip(FLAGS, combo))
    result = resolve_flags(state)
    if state["newCheckout"] and not state["payment_v2"]:
        assert result == "missing_dependency"
    elif state["newCheckout"] and state["legacyCheckout"]:
        assert result == "conflict"
    else:
        assert result == "ok"


def test_default_production_state_is_valid():
    prod = {f: bool(cfg.get("targeting", {}).get("percentage", 0) > 0)
            for f, cfg in CONFIG.items()}
    assert resolve_flags(prod) == "ok"


def test_flag_matrix_documented():
    assert len(FLAGS) >= 2, "matrix needs at least two flags to interact"
    for flag, cfg in CONFIG.items():
        assert "targeting" in cfg, f"{flag} missing targeting config"
