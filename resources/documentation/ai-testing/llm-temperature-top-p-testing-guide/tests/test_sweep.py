"""Offline tests for the temperature x top-p sweep.

Run: pytest tests/ -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mock_llm import MockClient
from sweep import sweep, PROMPT


def test_temperature_zero_is_deterministic():
    result = sweep(MockClient(), grid=[(0.0, 1.0)], runs=10)
    assert result[(0.0, 1.0)] == 1


def test_high_temperature_produces_diversity():
    result = sweep(MockClient(), grid=[(1.0, 1.0)], runs=10)
    assert result[(1.0, 1.0)] > 1


def test_top_p_truncates_variation():
    result = sweep(MockClient(), grid=[(1.0, 0.2)], runs=20)
    assert 1 <= result[(1.0, 0.2)] <= 2


def test_default_grid_runs_all_cells():
    result = sweep(MockClient(), runs=3)
    assert len(result) == 3
    assert result[(0.0, 1.0)] == 1
    assert result[(1.0, 1.0)] >= 1


def test_longer_runs_reveal_rare_variants():
    client = MockClient()
    short = sweep(client, grid=[(0.9, 1.0)], runs=5)
    long = sweep(client, grid=[(0.9, 1.0)], runs=20)
    assert long[(0.9, 1.0)] >= short[(0.9, 1.0)]


def test_sweep_uses_prompt_corpus_cell():
    result = sweep(MockClient(), prompt=PROMPT, grid=[(0.5, 0.9)], runs=5)
    assert (0.5, 0.9) in result
