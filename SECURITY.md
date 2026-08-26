# Security Policy

Infrastructure Engineering Harness treats authorization, evidence provenance, approval, sandboxing and source-of-truth protection as hard security boundaries.

## Report privately

Please do **not** open a public issue for a vulnerability that could enable:

- secret or credential exposure;
- unauthorized production mutation;
- approval or human-gate bypass;
- monotonic guard bypass;
- sandbox escape or misleading sandbox-enforcement claims;
- external `reference_only` Skill execution or privilege escalation;
- forged evidence provenance or promotion of unverified data into `verified_facts`;
- source-of-truth rewrite through transcript/context learning;
- audit-log tampering that makes execution unreconstructable.

Use GitHub's private vulnerability reporting / Security Advisory flow when available for this repository. If that UI is unavailable, contact the maintainer through the GitHub profile without publishing exploit details.

## In scope

The reference implementation is not a production authorization service, but security bugs in its contracts, validators, runtime guards and examples are still in scope because downstream implementations may rely on those invariants.

## Out of scope

- model hallucination without a contract or guard bypass;
- third-party provider outages;
- vulnerabilities in an upstream reference project that are not vendored or executed by this repository.

## Disclosure expectations

A useful report should include the affected file/contract, impact, reproduction steps, and a safe proposed fix if available. Do not include real credentials or proprietary production data.
