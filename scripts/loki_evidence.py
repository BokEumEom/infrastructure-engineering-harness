#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.evidence.base import normalize_adapter_result
from adapters.evidence.loki import collect_loki_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only Loki evidence")
    parser.add_argument("--url", required=True, help="Loki base URL")
    parser.add_argument("--host-header", help="optional HTTP Host header for Gateway routing")
    parser.add_argument("--query-file", required=True, help="JSON object describing LogQL queries")
    parser.add_argument("--lookback-seconds", type=int, default=900)
    parser.add_argument("--output", help="write normalized evidence JSON to this path")
    args = parser.parse_args()

    query_path = Path(args.query_file).expanduser().resolve()
    queries = json.loads(query_path.read_text(encoding="utf-8"))
    if not isinstance(queries, dict) or not queries:
        raise SystemExit("Loki query file must contain a non-empty JSON object")

    headers = {"Host": args.host_header} if args.host_header else None
    result = collect_loki_evidence(
        base_url=args.url,
        queries=queries,
        lookback_seconds=args.lookback_seconds,
        headers=headers,
        scope={"query_file": str(query_path), "host_header": args.host_header},
    )
    payload = normalize_adapter_result(result)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Evidence written: {output}", file=sys.stderr)
        print(f"Observations: {len(result['observations'])}", file=sys.stderr)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
