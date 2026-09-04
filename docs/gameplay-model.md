# NEngine.Gameplay — Reusable Gameplay Model

## Purpose

This document is an orientation to the reusable gameplay model owned by `NEngine.Gameplay`. It is not a complete gameplay design bible and it is not a specification of any particular game. Game-specific narrative, quests, regions, balancing, and content live in the consuming game — not here.

Cross-repository authority (product roadmap, migration sequencing, ownership map) remains with the CurseBreaker superproject.

## Layering

```text
Reusable gameplay meaning        (Gameplay domain)
        +
Renderer-independent runtime      (World / ECS)
        =
NEngine.Gameplay
        ↓
consumed by a game-specific runtime (e.g. CurseBreaker)
```

Both layers live in this repository. They are conceptually distinct but not necessarily separate targets.

## Core concepts

The following concepts are the accepted target ownership of `NEngine.Gameplay`. Some are already implicit in the accepted architecture; none are physically implemented in this repository yet. This is a target ownership projection, not a current implementation catalogue.

### Identity and world

- **World / ECS.** Renderer-independent runtime container for gameplay entities, components, and systems.
- **Entity identity.** A stable gameplay `EntityId` distinct from authoring-time editor identity. Runtime identity is not the same as the `SceneEntityRef` used by an authoring tool.
- **Transform / spatial state.** Authoritative runtime position/orientation for gameplay entities.
- **Physics / collision / navigation.** Authoritative gameplay-relevant spatial queries and constraints. Presentation may render them but does not own them.

### Interaction, items, capabilities

- **Interaction / Capabilities.** Reusable substrate for how entities expose behaviour to other entities (players, agents).
- **Items / Inventory / Storage.** Reusable substrate for ownership, transfer, and containers.

### Domain state

- **Facts.** Reusable knowledge/state representation.
- **Stories / Tasks / Codex.** Reusable structured progression substrate. Concrete quests, task text, and codex entries are game-specific content.
- **Relationships.** Reusable substrate for inter-actor state.
- **Perks / progression.** Reusable substrate for learnable capabilities.
- **Effects / status.** Reusable substrate for time-bounded or conditional modifiers.

### Behaviour and orchestration

- **AI foundations.** Perception, activity, directive, schedule concepts and the C++ AI-action lifecycle.
- **Event Chain runtime.** Reusable authored gameplay orchestration substrate.
- **Yarn runtime.** Reusable narrative orchestration substrate (game-specific commands/queries live in the consuming game).
- **Lua schedule host.** Reusable AI schedule execution substrate.

### Persistence-facing state

The gameplay-facing shape of persistence lives here: what is authoritative, what is transient, what must survive save/load, and what should be rebuilt on load. Actual on-disk save formats and game-specific save policy live outside this repository.

## Boundaries that must be preserved

- **Gameplay `EntityId` is not editor `SceneEntityRef`.** Runtime identity and authoring identity are semantically distinct even if a shared low-level typed-ID primitive from `NEngine.Core` is eventually used.
- **Dynamic gameplay state is not authored/static presentation state.** Reusable gameplay owns dynamic authoritative state; authored assets/definitions live in the consuming game's content repository.
- **`NEngine.Gameplay` acquires no Babylon, editor, or CurseBreaker dependency** to solve a presentation problem. Renderer integration, camera behaviour, materials, editor authoring, and native-host concerns belong to the consuming game.
- **No universal `Entity` ID for editor + authored docs + ECS runtime** is introduced by this repository.
- **No universal script-engine owner.** Yarn / Event Chain / Lua substrates each remain distinct; game-specific bridges live in the consuming game.

## Consumer integration shape

A consuming game (for example CurseBreaker) is expected to:

- depend on `NEngine.Gameplay` at build time;
- compose reusable gameplay substrate with its own game-specific rules, content, presentation, editor, and native host;
- own its own authoritative game-specific derivations (curse progression, act transitions, hub/service integration, etc.);
- never push game-specific concepts back into `NEngine.Gameplay` for generality's sake.

## Status

No production gameplay implementation exists in this repository yet. The projection above defines target ownership and reusable-model boundary. Concrete implementation lands incrementally through CurseBreaker migration `MIG-02` and subsequent product milestones as reusable surfaces become real.
