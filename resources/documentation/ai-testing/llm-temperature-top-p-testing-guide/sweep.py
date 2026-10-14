"""Temperature x top-p sweep for LLM output consistency.

Companion to https://qapractices.com/documentation/llm-temperature-top-p-testing-guide/

Runs the same prompt N times per (temperature, top_p) grid cell and prints
how many unique outputs each cell produced — the basic consistency metric
from the guide. Works with the real OpenAI client or with the offline
MockClient from mock_llm.py.

Usage:
    export OPENAI_API_KEY=sk-...
    python sweep.py              # real API
    python sweep.py --mock       # offline, no API key
"""

import argparse
import sys

GRID = [(0.0, 1.0), (0.7, 0.9), (1.0, 1.0)]
PROMPT = "Summarize why flaky tests erode trust in CI in one sentence."
RUNS = 5


def sweep(client, prompt=PROMPT, grid=GRID, runs=RUNS, model="gpt-4o-mini"):
    """Return { (temperature, top_p): unique_output_count } for the grid."""
    results = {}
    for temperature, top_p in grid:
        outputs = {
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
                max_tokens=60,
            ).choices[0].message.content.strip()
            for _ in range(runs)
        }
        results[(temperature, top_p)] = len(outputs)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="run offline against mock_llm.MockClient")
    args = parser.parse_args()

    if args.mock:
        from mock_llm import MockClient
        client = MockClient()
    else:
        from openai import OpenAI
        client = OpenAI()  # reads OPENAI_API_KEY

    for (temperature, top_p), unique in sweep(client).items():
        print(f"temp={temperature} top_p={top_p}: {unique}/{RUNS} unique")


if __name__ == "__main__":
    sys.exit(main())
