#!/usr/bin/env python3
"""Validate provider-neutral infrastructure context and repository contracts."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

def load(path: Path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in {".yaml", ".yml"} else json.loads(text)

def validate(path: Path, schema_name: str) -> list[str]:
    schema = load(SCHEMAS / schema_name); data = load(path)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data), key=lambda e: list(e.absolute_path))
    return [f"{path}: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("context", type=Path); args=parser.parse_args(); context=args.context
    targets=[(context/"service-catalog.yaml","service-catalog.schema.json")]
    targets += [(p,"policy.schema.json") for p in sorted((context/"policies").glob("*.y*ml"))]
    targets += [(p,"adr.schema.json") for p in sorted((context/"adr").glob("*.y*ml"))]
    targets += [(p,"incident.schema.json") for p in sorted((context/"incidents").glob("*.y*ml"))]
    for name,schema in {
      "sre.yaml":"sre-profile.schema.json",
      "devops.yaml":"devops-profile.schema.json",
      "finops.yaml":"finops-profile.schema.json",
      "security.yaml":"security-profile.schema.json"
    }.items():
        path=context/"domains"/name
        if path.exists(): targets.append((path,schema))
    repository_targets=[
      (ROOT/"examples/evidence/dependency-saturation.json","evidence.schema.json"),
      (ROOT/"examples/change-proposal.json","change-proposal.schema.json"),
      (ROOT/"evals/standard/incident-scenarios.json","eval-suite.schema.json"),
      (ROOT/"examples/ticketing/ticket-request.json","ticket-request.schema.json"),
      (ROOT/"examples/ticketing/ticket-policy.yaml","ticket-policy.schema.json"),
      (ROOT/"examples/loops/incident-response-state.json","loop-state.schema.json"),
      (ROOT/"examples/eval-output/loop-incident-recovered.json","loop-result.schema.json"),
      (ROOT/"evals/loops/standard.json","loop-eval-suite.schema.json"),
      (ROOT/"skill-evals/incident-analysis/evals.json","skill-eval-suite.schema.json"),
      (ROOT/"skill-evals/fixtures/incident-analysis.paired.json","skill-paired-experiment.schema.json")]
    repository_targets += [(p,"domain-eval-suite.schema.json") for p in sorted((ROOT/"evals/domains").glob("*.json"))]
    repository_targets += [(p,"loop-spec.schema.json") for p in sorted((ROOT/"loops").glob("*/loop.yaml"))]
    failures=[]
    for path,schema in targets+repository_targets:
        if not path.exists(): failures.append(f"missing required file: {path}")
        else: failures.extend(validate(path,schema))
    if failures:
        print("VALIDATION FAILED")
        for failure in failures: print(f"- {failure}")
        return 1
    print(f"VALIDATION PASSED ({len(targets)+len(repository_targets)} documents)"); return 0

if __name__ == "__main__": raise SystemExit(main())
