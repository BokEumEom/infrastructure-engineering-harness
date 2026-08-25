# Security Review Workflow

Use this workflow for architecture, delivery, infrastructure, agent/MCP, identity or external-integration changes where security constraints are material.

```text
Context + Evidence
      ↓
Security Review
      ↓
Trust / Identity / Data / Supply-chain Delta
      ↓
Open Risk or Missing Evidence?
   ┌──┴────────────┐
  yes              no
   ↓                ↓
block / verify   required controls
                    ↓
             Change Review / Proposal
                    ↓
             Independent Approval
                    ↓
              External Execution
                    ↓
          Post-change Verification
                    ↓
            Regression Obligations
```

## Required review outputs

- evidence references
- trust-boundary changes
- identity and privilege changes
- sensitive-data movement
- external integration/tool scope
- supply-chain requirements where applicable
- open risks and assumptions
- required controls
- human/policy gates
- security regression obligations

## External capability references

Third-party Security/DevOps Skills may provide implementation patterns, but they remain subject to `capabilities/registry.yaml` and `skills/capability-routing/SKILL.md`.

A reference Skill may inform a local artifact; it cannot independently authorize or verify a production security state.
