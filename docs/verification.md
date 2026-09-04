# NEngine.Gameplay — Local Verification

## Canonical command

```text
python scripts/verify_repo.py
python scripts/verify_repo.py --json
```

The verifier is standalone Python (stdlib only), read-only, and offline. It does not fetch, reset, clean, stash, install, or repair. It observes and reports.

## Current checks

| Check ID | Purpose |
|---|---|
| `docs.required` | Required local documentation files exist (`README.md`, `docs/architecture.md`, `docs/gameplay-model.md`, `docs/development.md`, `docs/verification.md`, `AGENTS.md`, `CLAUDE.md`). |
| `docs.links` | Relative Markdown links in canonical local docs resolve to files inside this repository. |
| `agent.contract` | `AGENTS.md` names the repository, lists local authority documents, references the verification command, and states forbidden dependencies. |
| `agent.claude-router` | `CLAUDE.md` routes to `AGENTS.md` and is short (adapter, not a duplicate contract body). |
| `repo.git-state` | Repository Git state is observable; a clean working tree is `PASS`, a dirty working tree is `WARNING`. |
| `paths.portable` | Canonical local documents contain no machine-specific absolute paths (`C:\Users\…`, `/Users/…`). |
| `dependencies.boundary` | Deterministic scan of any dependency-bearing configuration for forbidden project-layer names. Reports `PASS` with a deferred-to-migration note when no dependency-bearing configuration currently exists, so intentional not-yet-created migration surfaces are not treated as failures. |

## Deferred checks

These surfaces do not currently exist in this repository. They are established during CurseBreaker migration and are not fabricated by the local verifier:

- CMake or equivalent configure / build (`MIG-01` / `MIG-02`)
- unit / repository test surface (`MIG-01` / `MIG-02`)
- integration verification against `NEngine.Core` (`MIG-02` / later)
- cross-repository integration verification (CurseBreaker `MIG-07` / `MIG-08`)

Until they exist, corresponding checks are absent from the verifier rather than reported as `PASS` or `FAIL`.

## Result model

Per-check result:

- `PASS` — the check was executed and satisfied.
- `WARNING` — the check was executed and produced a non-blocking finding.
- `FAIL` — the check was executed and not satisfied.
- `UNKNOWN` — the check could not be evaluated because of missing prerequisites.

Aggregate overall:

- `HEALTHY` — no `FAIL`, no `UNKNOWN`, no `WARNING`.
- `DEGRADED` — no `FAIL`, no `UNKNOWN`, but at least one `WARNING`.
- `UNHEALTHY` — at least one `FAIL` or `UNKNOWN`.

## Exit codes

- `0` — `HEALTHY` or `DEGRADED` (no structural failure).
- `1` — `UNHEALTHY` (at least one structural failure).
- `2` — the verifier itself failed to execute. Distinct from a project verification failure.

## Read-only behaviour

The verifier never mutates the working tree, does not touch Git remotes, does not update submodules, does not install dependencies, and does not create permanent caches.

## Relationship to CurseBreaker task verification

Local verification produces evidence; it does not own task completion. When this repository is changed as part of a CurseBreaker task, closeout applies the CurseBreaker Verification Contract in addition to the local verifier. The local command remains a stable adapter surface so that future migration can extend what it verifies without changing the agent-facing contract.

## Future extension

Future migration surfaces (build, unit tests, integration proofs) may be added to `scripts/verify_repo.py` as they become real. The canonical command must remain `python scripts/verify_repo.py` and the aggregate/exit-code contract above must remain stable.

## JSON output schema

`python scripts/verify_repo.py --json` emits:

```json
{
  "schemaVersion": 1,
  "repository": "NEngine.Gameplay",
  "overall": "HEALTHY",
  "summary": {"pass": 0, "warning": 0, "fail": 0, "unknown": 0},
  "checks": [
    {"id": "docs.required", "status": "PASS", "message": "…"}
  ]
}
```

Field names may adapt additively; `schemaVersion` increases on any breaking change.
