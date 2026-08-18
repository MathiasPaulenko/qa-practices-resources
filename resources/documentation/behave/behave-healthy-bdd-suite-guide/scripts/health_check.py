"""Simple Behave suite health check."""
import ast
import os
import re
import subprocess
from collections import defaultdict


def run_behave_counts():
    result = subprocess.run(
        ["behave", "--dry-run", "--no-capture"],
        capture_output=True,
        text=True,
    )
    counts = {"features": 0, "scenarios": 0, "steps": 0}
    for line in result.stdout.splitlines():
        m = re.search(
            r"(\d+) features? passed, \d+ failed, \d+ skipped, (\d+) untested",
            line,
        )
        if m:
            counts["features"] = int(m.group(1)) + int(m.group(2))
        m = re.search(
            r"(\d+) scenarios? passed, \d+ failed, \d+ skipped, (\d+) untested",
            line,
        )
        if m:
            counts["scenarios"] = int(m.group(1)) + int(m.group(2))
        m = re.search(
            r"(\d+) steps? passed, \d+ failed, \d+ skipped, (\d+) untested",
            line,
        )
        if m:
            counts["steps"] = int(m.group(1)) + int(m.group(2))
    return counts


def collect_step_patterns():
    patterns = defaultdict(list)
    steps_dir = "features/steps"
    for root, _, files in os.walk(steps_dir):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                            if dec.func.id in {"given", "when", "then", "step"}:
                                if dec.args and isinstance(dec.args[0], ast.Constant):
                                    pattern = dec.args[0].value
                                    patterns[pattern].append(path)
    return patterns


def find_tag_smells():
    risky = []
    for root, _, files in os.walk("features"):
        for name in files:
            if not name.endswith(".feature"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            for line in text.splitlines():
                if line.strip().startswith("@"):
                    tags = {t.strip() for t in line.strip().split("@") if t.strip()}
                    if "flaky" in tags or "quarantine" in tags or "slow" in tags:
                        risky.append((path, line.strip()))
    return risky


def main():
    counts = run_behave_counts()
    patterns = collect_step_patterns()
    risky = find_tag_smells()

    duplicates = {
        p: paths
        for p, paths in patterns.items()
        if len(paths) > 1
    }

    step_count = len(patterns)

    print("=== Behave Suite Health Check ===")
    print(f"Features: {counts['features']}")
    print(f"Scenarios: {counts['scenarios']}")
    print(f"Steps: {counts['steps']}")
    print(f"Unique step patterns: {step_count}")
    print()

    if duplicates:
        print("Duplicate step patterns:")
        for pattern, paths in duplicates.items():
            print(f"  '{pattern}' in {paths}")
    else:
        print("No duplicate step patterns found.")

    if risky:
        print("\nRisky tags:")
        for path, tags in risky:
            print(f"  {path}: {tags}")
    else:
        print("\nNo risky tags found.")


if __name__ == "__main__":
    main()
