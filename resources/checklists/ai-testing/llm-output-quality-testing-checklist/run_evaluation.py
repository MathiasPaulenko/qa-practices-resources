"""Run the output-quality evaluation over a corpus.

Offline mode (default) scores the recorded model outputs in
mock_model_outputs.json. Live mode queries a real chat endpoint when
CHAT_API_URL is set, sampling each prompt three times at production
temperature so the consistency scorer sees real sampling variance.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from quality_evaluator import evaluate_case

BASE = Path(__file__).resolve().parent


def load_json(name: str) -> object:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def live_answers(prompt: str, runs: int = 3) -> list[str]:
    """Query a real endpoint; requires CHAT_API_URL and requests."""
    import requests

    url = os.environ["CHAT_API_URL"]  # e.g. http://localhost:8000/chat
    return [
        requests.post(url, json={"prompt": prompt}, timeout=30).json()["answer"]
        for _ in range(runs)
    ]


def main() -> int:
    cases = load_json("eval_prompts.json")
    live = bool(os.environ.get("CHAT_API_URL"))
    recorded = {} if live else load_json("mock_model_outputs.json")
    failures = 0
    for case in cases:
        answers = (
            live_answers(case["prompt"])
            if live
            else recorded.get(case["id"], [""])
        )
        result = evaluate_case(case, answers)
        status = "PASS" if result["passed"] else "FAIL"
        failures += 0 if result["passed"] else 1
        score_str = ", ".join(
            f"{k}={v:.2f}" for k, v in result["scores"].items()
        )
        print(f"{result['id']} [{result['dimension']}] {status} ({score_str})")
    print(f"\n{len(cases) - failures}/{len(cases)} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
