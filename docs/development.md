# NEngine.Gameplay Development

## Purpose

This document describes how to work inside `NEngine.Gameplay` today. It is a repository-local development contract; cross-repository product decisions, milestone sequencing, and migration classifications remain owned by the CurseBreaker superproject.

## Current state

Bootstrap repository. The repository contains its README, this documentation set, and reserved-empty layout directories (`include/`, `src/`, `tests/`, `scripts/`). No production gameplay or ECS implementation has been migrated yet.

## Repository layout

```text
NEngine.Gameplay/
├── README.md
├── docs/
│   ├── architecture.md      — repository role and dependency boundary
│   ├── gameplay-model.md    — reusable gameplay model orientation
│   └── development.md       — this document
├── include/                 — reserved for future public headers
├── src/                     — reserved for future implementation
├── tests/                   — reserved for future Gameplay tests
└── scripts/                 — reserved for repository-local tooling
```

Reserved directories currently contain `.gitkeep` files only. Production content lands during CurseBreaker migration `MIG-02` (Reusable C++ Foundation Migration) and later product milestones.

## Dependency expectations

`NEngine.Gameplay` may depend on:

- `NEngine.Core`
- the C++ standard library
- explicit, minimal third-party libraries introduced with justification

`NEngine.Gameplay` must not depend on:

- CurseBreaker-specific runtime, presentation, editor, or content
- Babylon or any other renderer/presentation technology
- authoring/editor implementation
- game-specific data or semantics

When placement is ambiguous, the accepted conservative rule is **unsure Gameplay vs CurseBreaker → CurseBreaker**.

## Build / test surface

Local build and test commands are **not established yet**. No CMake project, package manifest, test harness, or CI configuration currently exists.

Expected establishment:

| Surface | Introduced by |
|---|---|
| Build entry point (CMake or equivalent) | CurseBreaker migration `MIG-02` |
| Test entry point | Same migration stage, alongside the first real Gameplay module |
| Repository-local tooling | Added incrementally with real needs |

Do not fabricate build or test commands. Consumers of `NEngine.Gameplay` should assume nothing until the migration establishes concrete entry points.

## How other repositories consume Gameplay

When real gameplay modules land:

- consumers depend on Gameplay through a well-defined build/package mechanism established during migration;
- consumers do not reach into `src/`;
- consumers respect the accepted dependency direction `Core → Gameplay → Game`;
- consumers own their game-specific derivations (curse progression, act transitions, hub/service policy, etc.) rather than pushing them back into this repository for generality.

`CurseBreaker` is the first consumer. Additional consumers may appear only if they genuinely share reusable gameplay meaning — not because code is convenient.

## Contribution guidance

Code enters `NEngine.Gameplay` only when its semantics are:

- reusable gameplay meaning (not a single game's policy);
- renderer-independent;
- authoring/editor-independent;
- stable enough to be relied on by a consuming game.

"Might be reused" is not sufficient. Prefer keeping code in the consuming game until a real second consumer or a genuinely generic pattern appears.

## Cross-repository authority

Repository-local documentation is the appropriate authority for repository-internal development facts. Cross-repository product, ownership, migration, and verification decisions remain governed by the CurseBreaker superproject.
