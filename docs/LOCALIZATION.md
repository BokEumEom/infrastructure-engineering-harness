# Localization Policy

Infrastructure Engineering Harness supports localized **entry documentation** without duplicating every technical contract.

## Supported languages

| Language | README | Quickstart | Status |
| --- | --- | --- | --- |
| English | `README.md` | `QUICKSTART.md` | canonical |
| Korean | `README.ko.md` | `QUICKSTART.ko.md` | supported |
| Japanese | `README.ja.md` | `QUICKSTART.ja.md` | supported |
| Simplified Chinese | `README.zh-CN.md` | `QUICKSTART.zh-CN.md` | supported |

## Canonical source

English remains the canonical language for machine-readable schemas, Skills, architecture contracts, policies and evaluation definitions. This prevents four independent copies of safety-critical engineering rules from drifting.

Localized README and Quickstart files are first-class user entry points. They should communicate the same current product status, public CLI, major architecture primitives, safety boundaries and contribution paths.

## Required parity markers

Every localized README must preserve the meaning of:

- `Research Preview` status;
- `Resource Graph`;
- `Bound Capability`;
- `Runtime Kernel`;
- `Skill Lift / Context Lift`;
- `Paperthin` / Artifact Reflex;
- independent production authorization;
- fixture vs live validation distinction;
- `CONTRIBUTING.md` and Validation Report paths.

Every localized Quickstart must preserve:

- `harness setup`;
- `harness demo`;
- `harness validate`;
- `harness scenario`;
- `harness doctor`;
- Windows `harness.cmd` path;
- the statement that deterministic demo results are not live-agent effectiveness evidence.

## Translation scope

Do not translate every file by default. Add a localized technical document only when the translated version has a clear owner and maintenance value.

Prefer:

```text
Canonical technical contract
        ↓
Localized README / Quickstart
        ↓
Link to canonical detailed docs
```

rather than four independent copies of every schema, Skill and policy.

## Contribution

Translation fixes are valid contributions. A translation PR should:

1. preserve technical terms when translating them would create ambiguity;
2. keep file paths, command names, schema names and rule identifiers exact;
3. never weaken safety or authorization language;
4. update all affected entry documents when the public CLI or status changes;
5. pass `python scripts/check_localization.py` or `./harness validate`.

A no-op translation review is useful when the localized document already matches the canonical meaning.
