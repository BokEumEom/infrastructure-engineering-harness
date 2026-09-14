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
from adapters.evidence.tempo import collect_tempo_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only Tempo evidence")
    parser.add_argument("--url", required=True, help="Tempo base URL")
    parser.add_argument("--host-header", help="optional HTTP Host header for Gateway routing")
    parser.add_argument("--search-file", required=True, help="JSON object describing Tempo searches")
    parser.add_argument("--lookback-seconds", type=int, default=900)
    parser.add_argument("--trace-id", help="optional exact trace ID to fetch")
    parser.add_argument("--output", help="write normalized evidence JSON to this path")
    args = parser.parse_args()

    search_path = Path(args.search_file).expanduser().resolve()
    searches = json.loads(search_path.read_text(encoding="utf-8"))
    if not isinstance(searches, dict) or not searches:
        raise SystemExit("Tempo search file must contain a non-empty JSON object")

    headers = {"Host": args.host_header} if args.host_header else None
    result = collect_tempo_evidence(
        base_url=args.url,
        searches=searches,
        lookback_seconds=args.lookback_seconds,
        trace_id=args.trace_id,
        headers=headers,
        scope={"search_file": str(search_path), "host_header": args.host_header},
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
