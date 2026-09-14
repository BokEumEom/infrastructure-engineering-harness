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


def _trace_ids_from_bundle(path: Path, *, limit: int) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"trace ID source must contain a JSON object: {path}")
    ordered: list[str] = []
    for observation in payload.get("observations", []):
        if not isinstance(observation, dict):
            continue
        value = observation.get("value")
        if not isinstance(value, dict):
            continue
        for raw in value.get("trace_ids") or []:
            trace_id = str(raw or "").strip()
            if trace_id and trace_id not in ordered:
                ordered.append(trace_id)
            if len(ordered) >= limit:
                return ordered
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only Tempo evidence")
    parser.add_argument("--url", required=True, help="Tempo base URL")
    parser.add_argument("--host-header", help="optional HTTP Host header for Gateway routing")
    parser.add_argument("--search-file", required=True, help="JSON object describing Tempo searches")
    parser.add_argument("--lookback-seconds", type=int, default=900)
    parser.add_argument("--trace-id", action="append", default=[], help="exact trace ID to fetch; may be repeated")
    parser.add_argument("--trace-id-file", help="normalized evidence JSON containing value.trace_ids to follow up exactly")
    parser.add_argument("--max-trace-ids", type=int, default=20, help="maximum exact trace IDs to follow from --trace-id-file")
    parser.add_argument("--output", help="write normalized evidence JSON to this path")
    args = parser.parse_args()

    if args.max_trace_ids < 1 or args.max_trace_ids > 100:
        raise SystemExit("--max-trace-ids must be between 1 and 100")

    search_path = Path(args.search_file).expanduser().resolve()
    searches = json.loads(search_path.read_text(encoding="utf-8"))
    if not isinstance(searches, dict) or not searches:
        raise SystemExit("Tempo search file must contain a non-empty JSON object")

    requested = [str(value).strip() for value in args.trace_id if str(value).strip()]
    trace_id_file = None
    if args.trace_id_file:
        trace_id_file = Path(args.trace_id_file).expanduser().resolve()
        for trace_id in _trace_ids_from_bundle(trace_id_file, limit=args.max_trace_ids):
            if trace_id not in requested:
                requested.append(trace_id)
            if len(requested) >= args.max_trace_ids:
                break

    headers = {"Host": args.host_header} if args.host_header else None
    result = collect_tempo_evidence(
        base_url=args.url,
        searches=searches,
        lookback_seconds=args.lookback_seconds,
        trace_ids=requested[: args.max_trace_ids],
        headers=headers,
        scope={
            "search_file": str(search_path),
            "host_header": args.host_header,
            "trace_id_file": str(trace_id_file) if trace_id_file else None,
            "exact_trace_ids_requested": len(requested[: args.max_trace_ids]),
        },
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
