# Knowledge Consolidation

Infrastructure Engineering Harness separates what was observed, what was independently verified, what an engineer or agent infers, and what the organization has accepted as durable truth.

This is intentionally stricter than a generic memory layer.

```text
Observation
    ↓ independent verification
Verified Fact
    ↓ engineering reasoning
Engineering Assessment
    ↓ outcome evidence / repeated use
Learning Candidate
    ↓ governance
Durable Organizational Knowledge
```

## Epistemic classes

| Class | Meaning | May be written by an agent? | Durable source of truth? |
| --- | --- | --- | --- |
| Observation | Raw or normalized signal from an environment, tool, human, or test | Yes, as a captured signal | No |
| Verified Fact | Claim supported by independent evidence | Only through verifier-controlled promotion | No, unless separately adopted |
| Engineering Assessment | Interpretation, hypothesis, risk judgment, or recommendation | Yes | No |
| Learning Candidate | Proposed reusable lesson derived from a Loop outcome | Yes, as a proposal | No |
| Durable Knowledge | ADR, Policy, Runbook, Service Catalog, approved incident learning, or other governed truth | No silent overwrite | Yes |

`Observation != Verified Fact != Assessment != Durable Knowledge`.

An agent must never hide an unverified assessment inside authoritative language.

## Hot and cold learning

The harness adopts a hot/cold distinction inspired by persistent agent-memory systems without treating conversational memory as engineering truth.

### Hot learning

Hot learning is recent, task-local, and provisional:

- verified facts from the current Loop;
- failed hypotheses;
- successful or failed procedures;
- human decisions;
- regression results;
- unresolved evidence gaps.

Hot learning is useful for the next iteration and for candidate generation. It is not automatically promoted into ADRs, Policies, Runbooks, or Service Catalog.

### Cold knowledge

Cold knowledge is governed, durable, and intentionally maintained:

- Architecture and ADRs;
- Policies;
- Service Catalog;
- approved Runbooks;
- incident records and reviewed postmortems;
- evaluation scenarios and negative corpus entries;
- approved operating procedures.

Promotion from hot learning to cold knowledge requires the normal owner/review path for that artifact type.

## Learning Candidate contract

`schemas/knowledge-candidate.schema.json` defines the proposed writeback shape. A candidate must identify:

- epistemic class;
- source Loop/run;
- supporting and contradicting evidence;
- confidence without pretending confidence is verification;
- target artifact type;
- required review;
- freshness/expiry hints where applicable.

A candidate may be rejected, merged with an existing artifact, superseded, or promoted.

## Negative corpus

Failed hypotheses and prohibited paths are first-class learning.

Example:

```yaml
claim: high_cpu_implies_root_cause
epistemic_class: engineering_assessment
status: disproven
evidence:
  - incident/INC-123/db-lock-analysis
target:
  type: eval_candidate
```

The concrete incident is evidence. The durable lesson should generalize the failure mode enough to stop the next Loop from repeating it.

## Consolidation

A consolidator may:

1. group candidates by service, resource, failure mode, or policy domain;
2. deduplicate semantically equivalent candidates;
3. identify contradictions;
4. separate stable facts from assessments;
5. propose a target artifact update;
6. preserve provenance and source Loop ids;
7. require the artifact owner's normal review.

A consolidator must not:

- promote `verified_by: agent`;
- convert confidence into verification;
- erase contradictory evidence;
- rewrite protected source-of-truth artifacts without review;
- treat repeated model output as independent evidence.

## Relationship to Loop Engineering

Loop termination creates a reviewable learning boundary:

```text
Verified Outcome / Escalation / Failure
                  ↓
           Learning Capture
                  ↓
          Knowledge Candidate
                  ↓
             Consolidate
                  ↓
          Review / Promote
                  ↓
      Organizational Knowledge
                  ↓
              Next Loop
```

The next Loop may consume promoted knowledge and recent hot learning through a bounded Context Pack.
