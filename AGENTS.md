# NEngine.Gameplay — Agent Contract

Repository-local agent contract. Read this first when working inside `NEngine.Gameplay`.

## Repository

`NEngine.Gameplay` — reusable, renderer-independent gameplay semantics and runtime. It is a standalone library; `CurseBreaker` is one consumer / integration project.

## Local documentation authority

Repository-local documents are authoritative for repository-internal development facts:

- [README.md](README.md) — repository landing page
- [docs/architecture.md](docs/architecture.md) — repository role and dependency boundary
- [docs/gameplay-model.md](docs/gameplay-model.md) — reusable gameplay model orientation
- [docs/development.md](docs/development.md) — repository-local development contract
- [docs/verification.md](docs/verification.md) — local verification contract

## Cross-repository authority

When this repository is being changed as part of the CurseBreaker integration project, cross-repository ownership, product roadmap, migration classification, orchestration policy, and architecture decisions crossing repository boundaries are governed by the CurseBreaker superproject. Standalone consumers may have their own integration governance.

If local rules appear to conflict with the CurseBreaker superproject cross-repository governance, stop and report the conflict — do not silently prefer whichever rule is easier.

## Dependency boundary

Allowed:

- `NEngine.Core`
- C++ standard library
- narrowly justified, explicitly introduced third-party libraries

Forbidden project-layer dependencies:

- `CurseBreaker` runtime, presentation, editor, or native host
- Babylon or any renderer / presentation technology
- editor implementation (VS Code extension, authoring tools, etc.)
- `CurseBreaker.Content` authored data consumed as a runtime dependency

Conservative routing rule: **unsure whether something belongs in Gameplay or CurseBreaker → prefer CurseBreaker (game-specific) ownership.**

## Reusable ownership areas

Target ownership of this repository (concept-level; see `docs/gameplay-model.md` for detail):

World / ECS, gameplay `EntityId`, `Transform`, physics / collision / navigation, Interaction / Capabilities, Items / Inventory / Storage, Facts / Stories / Tasks / Codex, Relationships, Perks / progression, Effects / status, AI foundations, Event Chain runtime, Yarn runtime, Lua schedule host, persistence-facing gameplay state.

These are **target ownership**, not necessarily current implementation.

## Identity and layering guardrails

- **Gameplay `EntityId` ≠ editor `SceneEntityRef`.** Runtime gameplay identity and authoring-time editor identity remain semantically distinct.
- **Dynamic gameplay state ≠ authored / static presentation data.** Reusable gameplay owns dynamic authoritative state; authored assets/definitions live in the consuming game's content repository.
- **No Babylon or editor dependency** may be pulled downward to solve a Gameplay problem.
- **No universal script-engine owner.** Yarn / Event Chain / Lua substrates remain distinct.

## Current implementation state

Bootstrap. `include/`, `src/`, `tests/`, and `scripts/` (aside from the local bootstrap tooling introduced by this contract) contain no production code. Real Gameplay code is expected to land during CurseBreaker migration stage `MIG-02` and subsequent product milestones.

## Local verification

Canonical command:

```text
python scripts/verify_repo.py
python scripts/verify_repo.py --json
```

Result model, exit codes, and current/deferred checks are documented in [docs/verification.md](docs/verification.md). The verifier is read-only and offline; it does not install tools, fetch, or repair.

Local verification produces evidence. It does not own task completion. When this repository is changed as part of a CurseBreaker task, the CurseBreaker Verification Contract and closeout own `COMPLETE`.

## Escalation

Escalate to the CurseBreaker superproject when a task would:

- introduce CurseBreaker-specific semantics into Gameplay;
- introduce Babylon, presentation, or editor dependencies;
- change the public architectural role of Gameplay;
- move ownership between Core and Gameplay or between Gameplay and CurseBreaker;
- require a migration classification change;
- introduce a cross-repository API change whose consumer contract is unclear.

Normal local implementation inside accepted Gameplay ownership should not require escalation.
