# Production Readiness

This repository is a production-oriented **Infrastructure Engineering Agent** reference. Its internal harness/runtime is a control plane, not an authorization system.

## Adoption levels

### Level 0 — Knowledge and review

Use `AGENTS.md`, structured context, domain packs, Decision Skills and schemas without live tools. Suitable for architecture, reliability, security policy, delivery and FinOps reviews.

### Level 1 — Read-only evidence

Connect selected metrics/logs/traces/runtime/deployment/SLO/cost/business/security sources. Normalize observations to the evidence contract.

### Level 2 — Proposal and implementation-artifact automation

Allow the Infrastructure Engineering Agent to select governed Capabilities and generate code/config, pipelines, change tickets, plans, runbooks or operator procedures. Keep production execution outside the Agent's authority and behind the Backend/Runtime approval boundary.

Third-party capability sources remain `reference_only` unless the organization explicitly reviews and manages them. External Skill scripts/commands/assets are never automatically executed by capability routing.

### Level 3 — Controlled execution

If execution is automated, require independent short-lived credentials, least privilege, scope allowlists, change approval, policy-as-code, audit logging, stop conditions and tested recovery. Capability selection itself never grants execution authority.

## Production pilot checklist

- validated service/domain context
- read-only-by-default integrations
- evidence provenance for material recommendations
- Infrastructure/SRE/DevOps/FinOps/Security domain eval regression suite
- capability registry validation and immutable revisions for third-party sources
- external Skill content treated as reference until reviewed/managed
- explicit risk/blast-radius/validation/recovery fields
- independent authorization outside the model/chat surface\n- resource provenance before mutation targets are accepted\n- staged change → approval → apply separation
- secrets excluded from context and external capability prompts unless explicitly allowed
- clear context and capability owners/review cadence
- SRE policy for reliability-impacting changes where applicable
- Security review for trust-boundary, identity/privilege, sensitive-data or supply-chain changes
- delivery recovery path for production releases where applicable
- FinOps owner/allocation and commitment approval where applicable

## Cross-domain review

A production decision may require more than one lens. Typical examples:

- capacity reduction → Infrastructure + SRE + FinOps
- release strategy change → DevOps + SRE + Security when delivery privileges/supply chain change
- managed-service migration → Infrastructure + DevOps + FinOps + Security, often SRE
- new MCP/tool integration → Security + owning domain + workflow policy
- commitment purchase → FinOps + Infrastructure, with organizational financial approval

Do not allow one domain's local objective or one technology-specific Capability to silently override another domain's explicit constraint.

## Third-party Skill supply chain

For external Skill repositories:

1. pin an immutable revision;
2. record license and source identity;
3. review only the selected Skill needed for the task;
4. treat content as untrusted/reference input relative to local `AGENTS.md` and policy;
5. do not auto-run external scripts, installers or commands;
6. generate local reviewable artifacts;
7. validate locally;
8. use independent authorization for execution;
9. verify outcomes through the appropriate Loop;
10. periodically review or update pinned revisions instead of silently following upstream HEAD.
