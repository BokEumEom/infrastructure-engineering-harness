#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.multisignal_review import correlate_multisignal_evidence


def read_json(path: str) -> dict:
    value = Path(path).expanduser().resolve()
    payload = json.loads(value.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object: {value}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Correlate Ops, Loki and Tempo evidence without changing the Ops decision")
    parser.add_argument("--ops-review", required=True)
    parser.add_argument("--loki", required=True)
    parser.add_argument("--tempo", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = correlate_multisignal_evidence(
        read_json(args.ops_review),
        read_json(args.loki),
        read_json(args.tempo),
    )
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Multi-signal review written: {output}", file=sys.stderr)
    else:
        print(rendered, end="")
    print(f"Status: {result['status']}", file=sys.stderr)
    print(f"Correlations: {result['correlation_count']}", file=sys.stderr)
    print(f"Decision effect: {result['decision_effect']}", file=sys.stderr)
    return 0 if not result["source_unavailable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
