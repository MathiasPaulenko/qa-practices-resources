"""LLM output checker for the AI Testing Checklist companion.

Sends a prompt to a chat model and asserts that expected phrases appear
in the answer while forbidden ones do not. Works against the real OpenAI
API (openai>=1.54) or the bundled MockClient for offline runs.
"""

import argparse
import json
import sys


def evaluate_llm(prompt, expected_patterns, forbidden_patterns, client=None, model="gpt-4o-mini"):
    """Return the model answer lowercased, or raise AssertionError on a failed check."""
    if client is None:
        from openai import OpenAI
        client = OpenAI()  # reads OPENAI_API_KEY from the environment
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        seed=42,
    )
    text = response.choices[0].message.content.lower()
    assert any(p in text for p in expected_patterns), f"Missing expected content: {text}"
    assert not any(p in text for p in forbidden_patterns), f"Forbidden content found: {text}"
    return text


def run_dataset(path, client=None, model="gpt-4o-mini"):
    """Run every case in a guardrail dataset; return (input, passed) tuples."""
    with open(path, encoding="utf-8") as fh:
        cases = json.load(fh)
    results = []
    for case in cases:
        try:
            evaluate_llm(case["input"], case["expected"], case["forbidden"], client=client, model=model)
            results.append((case["input"], True))
        except AssertionError:
            results.append((case["input"], False))
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the guardrail dataset against an LLM.")
    parser.add_argument("--dataset", default="guardrail_dataset.json")
    parser.add_argument("--mock", action="store_true", help="run offline against the bundled mock client")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    client = None
    if args.mock:
        from mock_llm import MockClient
        client = MockClient()

    results = run_dataset(args.dataset, client=client, model=args.model)
    failed = [text for text, ok in results if not ok]
    for text, ok in results:
        print(f"{'PASS' if ok else 'FAIL'}  {text}")
    sys.exit(1 if failed else 0)
