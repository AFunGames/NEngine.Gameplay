# NEngine.Gameplay Architecture

## Repository Role

`NEngine.Gameplay` is the reusable gameplay foundation shared across multiple games. It defines architectural boundaries for reusable gameplay semantics and runtime participation while remaining independent from any single game.

## Dependency Direction

Canonical direction:

```text
NEngine.Core
      ↓
NEngine.Gameplay
      ↓
Game-specific gameplay/runtime
```

`NEngine.Gameplay` may depend downward on `NEngine.Core` and must not depend upward on game-specific code.

## Conceptual Shape

```text
              NEngine.Core
                    ↓
             NEngine.Gameplay
              /          \
        Gameplay        World
           |             |
           +------┬------+
                  ↓
           Game-specific code
```

This is conceptual layering inside one repository. Gameplay and World may become separate CMake targets while remaining in the same repository.

## Gameplay Domain Layer

The Gameplay layer is for reusable gameplay-domain concepts and authoritative domain state that are not inherently ECS-bound.

## World / ECS Layer

The World layer is for renderer-independent runtime entity/component/system participation in gameplay.

## Gameplay vs World Boundary

- **Gameplay** answers what concepts mean and what rules/state apply.
- **World** answers how runtime entities/components participate in those concepts.

The domain layer must remain usable without forcing ECS ownership of all gameplay concepts.

## Renderer Independence

This repository is renderer-agnostic. Rendering engines, scene graph technology, UI frameworks, screen-space logic, and input backend specifics remain outside `NEngine.Gameplay`.

## Game-Specific Boundary

Game-specific stories, quests, balancing, regions, NPC behavior, and title-specific mechanics are intentionally excluded. Reusable primitives may be consumed by game-specific layers without importing game-specific semantics back into this repository.

## Persistence Principle

Future persistence should store authoritative gameplay/runtime state rather than transient execution machinery.

## Current Status

Bootstrap only. No production code, ECS implementation, build system, dependency selection, migration, or CI configuration has been added yet.
