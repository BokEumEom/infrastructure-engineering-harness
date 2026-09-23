# Documentation

This is the canonical documentation map for Infrastructure Engineering Agent.

Use progressive disclosure: start here, open the smallest relevant overview, and follow links to detail only when the task needs it. Do not load every document by default.

## Start here

- [5-minute Quickstart](../QUICKSTART.md) — install and run the local deterministic demo.
- [Architecture](ARCHITECTURE.md) — canonical system shape, ownership, and boundaries.
- [Release Status](RELEASE-STATUS.md) — what is implemented, experimental, or not promised.
- [Documentation Policy](DOCUMENTATION.md) — how documentation is structured, updated, checked, and reviewed.

## Architecture and contracts

- [Architecture](ARCHITECTURE.md) — synthesized architecture and control-plane boundary.
- [Capability Model](CAPABILITY-MODEL.md) — capability metadata, binding, trust, and availability.
- [Workflow Surface](WORKFLOW-SURFACE.md) — workflow-facing surface and execution boundaries.
- [Harness Unhobbling](HARNESS-UNHOBBLING.md) — minimal always-loaded guidance and progressive disclosure.
- [Knowledge Consolidation](KNOWLEDGE-CONSOLIDATION.md) — observation-to-durable-knowledge lifecycle.
- [Memory, Performance, and Release](MEMORY-PERFORMANCE-RELEASE.md) — memory, performance, and release contracts.
- [Artifact Reflexes](ARTIFACT-REFLEXES.md) — Paperthin-inspired artifact, SSOT, and evaluation hygiene.

## Operations and live evidence

- [Operations Review](OPS-REVIEW.md) — operational review behavior and decision boundaries.
- [Production Readiness](PRODUCTION-READINESS.md) — production-readiness requirements and limitations.
- [Kubernetes Live Evidence](KUBERNETES-LIVE-EVIDENCE.md) — Kubernetes evidence adapter contract.
- [Prometheus Live Evidence](PROMETHEUS-LIVE-EVIDENCE.md) — Prometheus evidence adapter contract.

## Evaluation and evidence

- [Skill Evaluation](SKILL-EVALUATION.md) — Skill effectiveness evaluation model.
- [Community Validation](COMMUNITY-VALIDATION.md) — reproducible community validation guidance.
- [Evidence index](evidence/README.md) — evidence, benchmark, and validation documentation entrypoint.

## Decisions

- [Decision records](decisions/README.md) — architecture and policy decisions that explain why the current state exists.

Architecture documents describe **what is true now**. Decision records describe **why a durable choice was made**.

## Research and reference models

- [Reference Models](REFERENCE-MODELS.md) — primary and supporting external models.
- [Ecosystem References](ECOSYSTEM-REFERENCES.md) — wider ecosystem references.
- [Commerce Agent Patterns](COMMERCE-AGENT-PATTERNS.md) — agent/backend/runtime patterns.
- [AWS AgentCore AIOps Patterns](AWS-AGENTCORE-AIOPS-PATTERNS.md) — production AIOps patterns and local implications.

## Project policy and status

- [Release Status](RELEASE-STATUS.md) — current maturity and release boundary.
- [Localization Policy](LOCALIZATION.md) — supported entry languages and canonical-language policy.
- [Documentation Policy](DOCUMENTATION.md) — documentation ownership, drift checks, and review loop.

## Navigation rule

README.md at the repository root is the project landing page. This file is the documentation router. Detailed documents own their subject matter.

When adding a document, place it under docs/, link it from the nearest relevant index, and avoid copying the same explanation into multiple overview pages.
