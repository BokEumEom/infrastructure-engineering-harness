# Production Readiness

This repository is a production-oriented engineering harness reference, not an authorization system.

## Adoption levels

### Level 0 — Knowledge and review

Use `AGENTS.md`, structured context, domain packs and schemas without live tools. Suitable for architecture, reliability policy, delivery and FinOps reviews.

### Level 1 — Read-only evidence

Connect selected metrics/logs/traces/runtime/deployment/SLO/cost/business sources. Normalize observations to the evidence contract.

### Level 2 — Proposal automation

Allow the agent to generate code/config, change tickets, plans, runbooks or operator procedures. Keep production execution outside the agent's authority.

### Level 3 — Controlled execution

If execution is automated, require independent short-lived credentials, least privilege, scope allowlists, change approval, policy-as-code, audit logging, stop conditions and tested recovery.

## Production pilot checklist

- validated service/domain context
- read-only-by-default integrations
- evidence provenance for material recommendations
- domain eval regression suite
- explicit risk/blast-radius/validation/recovery fields
- independent authorization outside the model
- secrets excluded from context
- clear context owners and review cadence
- SRE policy for reliability-impacting changes where applicable
- delivery recovery path for production releases where applicable
- FinOps owner/allocation and commitment approval where applicable

## Cross-domain review

A production decision may require more than one lens. Typical examples:

- capacity reduction → Infrastructure + SRE + FinOps
- release strategy change → DevOps + SRE
- managed-service migration → Infrastructure + DevOps + FinOps, often SRE
- commitment purchase → FinOps + Infrastructure, with organizational financial approval

Do not allow one domain's local objective to silently override another domain's explicit constraint.
