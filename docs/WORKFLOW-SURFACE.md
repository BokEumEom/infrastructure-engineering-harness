# Workflow Surface

The Harness has a deliberately simple user-facing workflow surface and a rigorous internal control plane. The surface provides entrypoints and discoverability; it does not prescribe the model's reasoning path.

The design is influenced by workflow-composed agent systems such as gstack: the user should not need to manually select every Skill when the intent already identifies the engineering workflow.

## User-facing intents

Canonical entry intents:

```text
incident
reliability
delivery
finops
security
change
learn
```

Future CLI/chat surfaces may expose these as:

```text
harness incident
harness reliability
harness delivery
harness finops
harness security
harness change
harness learn
```

Natural-language requests may route to the same entrypoints.

## Routing model

```text
User Intent
    ↓
Minimal seed context
    ↓
Model Judgment
   ↙        ↘
suggested      pull additional
Loop/Skill     context/capability
   ↘        ↙
      Action
        ↓
Runtime / verification boundary
```

Mappings are recommendations for discovery, not a mandatory chain. The model may skip irrelevant layers or choose another relevant Skill/Capability while hard Runtime, evidence, permission, and verification boundaries remain unchanged.

## Suggested mapping

| Intent | Primary Loop / workflow | Typical Skills |
| --- | --- | --- |
| incident | `incident-response` | incident-analysis, sre-review, ticketing |
| reliability | `reliability-improvement` | sre-review, architecture-review |
| delivery | `delivery-improvement` | delivery-review, change-review |
| finops | `finops-optimization` | finops-review, architecture-review |
| security | security-review workflow | security-review, change-review |
| change | `change-validation` | change-review, architecture-review |
| learn | knowledge consolidation | loop-engineering, artifact-hygiene, eval-integrity |

## Progressive disclosure

Users should see the engineering outcome, evidence gaps, approval gates, and next action. They should not need to understand internal schema names unless they ask.

A concise run summary should answer:

- what is known;
- what remains unknown;
- what the current assessment is;
- what evidence is required next;
- whether a human gate is pending;
- whether the Loop is done, waiting, escalated, or failed;
- what learning candidate was produced.

## No implicit authority

Routing a request to a workflow never grants permission.

A request such as "fix production" may select `change-validation`, but production mutation still requires independently authorized execution and any configured human gate.
