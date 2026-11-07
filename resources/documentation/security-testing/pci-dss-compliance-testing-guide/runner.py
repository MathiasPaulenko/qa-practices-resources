"""Evidence pack runner — executes control checks and writes a dated
evidence file an assessor can consume.

Usage:
    python runner.py --config controls.yaml

Produces evidence/evidence-YYYYMMDD.json with per-control results.
The config declares which checks run and against which targets, so the
same pack regenerates every quarter on schedule.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from controls.pan_sweep import sweep_path
from controls.segmentation_check import check_segmentation
from controls.tls_check import evaluate_tls, probe_tls


def run_pan_check(paths: list[str]) -> dict:
    findings = {}
    for p in paths:
        findings.update(sweep_path(Path(p)))
    return {
        "control": "req3-pan-sweep",
        "status": "fail" if findings else "pass",
        "files_with_findings": len(findings),
        "detail": {k: len(v) for k, v in findings.items()},
    }


def run_tls_check(targets: list[dict]) -> dict:
    results = []
    for t in targets:
        r = evaluate_tls(probe_tls(t["host"], t.get("port", 443)))
        results.append({
            "host": t["host"], "port": t.get("port", 443),
            "negotiated": r.negotiated, "cipher": r.cipher,
            "failures": r.failures,
        })
    failed = [r for r in results if r["failures"]]
    return {
        "control": "req4-tls",
        "status": "fail" if failed else "pass",
        "targets": results,
    }


def run_segmentation_check(targets: list[dict]) -> dict:
    results = []
    for t in targets:
        reachable = check_segmentation(t["host"], t.get("ports"))
        results.append({"host": t["host"], "reachable_ports": reachable})
    failed = [r for r in results if r["reachable_ports"]]
    return {
        "control": "req11-segmentation",
        "status": "fail" if failed else "pass",
        "targets": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="controls.yaml")
    parser.add_argument("--out", default="evidence")
    args = parser.parse_args()

    try:
        import yaml
        config = yaml.safe_load(Path(args.config).read_text())
    except ImportError:
        print("PyYAML required: pip install pyyaml")
        return 2

    results = []
    if "pan_paths" in config:
        results.append(run_pan_check(config["pan_paths"]))
    if "tls_targets" in config:
        results.append(run_tls_check(config["tls_targets"]))
    if "segmentation_targets" in config:
        results.append(run_segmentation_check(config["segmentation_targets"]))

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    pack = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "standard": "PCI DSS v4.0",
        "controls": results,
        "overall": "pass" if all(r["status"] == "pass" for r in results) else "fail",
    }
    dest = out_dir / f"evidence-{stamp}.json"
    dest.write_text(json.dumps(pack, indent=2))
    print(f"evidence written to {dest} — overall: {pack['overall']}")
    return 0 if pack["overall"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
