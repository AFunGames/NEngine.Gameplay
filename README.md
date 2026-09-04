# NEngine.Gameplay

## Status

Repository bootstrap / reusable gameplay architecture setup.

## Purpose

`NEngine.Gameplay` is a reusable C++ gameplay foundation for multiple games. It is intended to host both reusable gameplay-domain concepts and a renderer-independent gameplay World/ECS runtime.

## Architecture

```text
NEngine.Core
      ↓
NEngine.Gameplay
      ├── Gameplay domains
      └── World / ECS runtime
      ↓
Game-specific gameplay/runtime
```

## Gameplay vs World

- **Gameplay** = domain meaning, state, and rules.
- **World** = runtime entities, components, and systems that participate in gameplay.

## Dependency Rules

- `NEngine.Gameplay` may depend on `NEngine.Core`.
- `NEngine.Gameplay` must not depend on CurseBreaker or any other game-specific repository.
- `NEngine.Gameplay` must not depend on renderer or presentation technology.

## Renderer Independence

This repository is renderer-agnostic and must not encode rendering APIs, renderer-specific scene models, UI frameworks, or input backend details.

## Repository Structure

```text
.
├── docs/
├── include/
├── src/
├── tests/
├── scripts/
├── .editorconfig
├── .gitattributes
├── .gitignore
└── README.md
```

## Documentation

- [docs/architecture.md](docs/architecture.md) — repository role and dependency boundary
- [docs/gameplay-model.md](docs/gameplay-model.md) — reusable gameplay model orientation
- [docs/development.md](docs/development.md) — repository-local development contract

Repository-local documentation is authoritative for repository-internal development facts. Cross-repository product, ownership, and migration decisions remain governed by the CurseBreaker superproject.

## Current State

No production gameplay implementation exists yet. No ECS implementation, build topology, dependencies, tests, or CI have been introduced.

## Planned First Steps

1. Audit existing gameplay/runtime baselines and candidates.
2. Identify the first minimal reusable contracts.
3. Establish `NEngine.Core` dependency setup.
4. Introduce build topology with the first real module.
5. Implement or migrate incrementally with tests.
6. Keep game-specific semantics outside this repository.
