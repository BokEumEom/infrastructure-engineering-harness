# Security Pack

Use this pack when the primary question is trust, authorization, sensitive data, supply-chain integrity, attack surface, external integrations, or whether an infrastructure/delivery change weakens an existing security control.

## Context

Durable Security context lives in `.infra-context/domains/security.yaml` and conforms to `schemas/security-profile.schema.json`.

Current findings, vulnerability status, active attack indicators, access inventories and scan results belong in Evidence bundles rather than durable policy files.

## Core concepts

- asset and data classification
- trust boundaries and identity flows
- least privilege and separation of duties
- privileged/high-impact actions
- external/tool/MCP integrations
- software supply-chain provenance
- security controls and approved exceptions
- independent authorization and auditability

## Decision questions

1. Does this change introduce or cross a new trust boundary?
2. Does identity, privilege or authorization scope expand?
3. Does sensitive data move to a new component, tool, vendor or channel?
4. Is an external integration trusted for the requested data and actions?
5. Are privileged actions independently authorized and auditable?
6. Is supply-chain provenance sufficient for the artifact being promoted?
7. Are open security risks explicitly accepted, mitigated or blocking?
8. Which security guarantees must remain regression obligations after the change?

## Capability boundary

Technology-specific security references such as MCP hardening, threat modeling, SBOM tooling or policy-as-code may be selected through `capabilities/registry.yaml`. They do not override this domain's decision rules and do not gain execution authority by being registered.

## Workflow

See `workflows/security-review.md`.

## Eval

`evals/domains/security.json` tests privilege expansion, MCP/tool boundaries, sensitive-data movement, supply-chain trust, missing auditability, and approved exceptions.
