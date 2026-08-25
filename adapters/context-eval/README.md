# Agent Context Evaluation Adapters

The core harness does not depend on one transcript store or agent product.

A context-evaluation adapter may collect project-scoped sessions from Claude Code, Codex, Cursor, Kiro-compatible runtimes, `backpass`, or another local harness, but it should normalize only the evidence needed by the context-learning layer.

```text
Local transcript store
        ↓
Collector / distiller
        ↓
Secret redaction
        ↓
context-evidence.schema.json
        ↓
context-backpass
        ↓
Human-reviewed AGENTS.md proposal
```

## Adapter requirements

1. Match sessions to the correct repository/workspace before analysis.
2. Prefer deterministic distillation before model-based loss analysis.
3. Redact obvious secrets and credentials before producing evidence.
4. Preserve a local/opaque source reference and verbatim evidence quote for review.
5. Do not commit raw transcripts to this repository.
6. Fail soft when a transcript format is unsupported or changes.
7. Do not let transcript data directly mutate `AGENTS.md` or any source-of-truth context.

`backpass` is a useful reference implementation for local transcript collection and evidence-gated proposals, but it is not a required runtime dependency of this harness.

References:
- https://blog.kunchenguid.com/p/your-agentsmd-is-a-neural-net
- https://github.com/kunchenguid/backpass
