# Claude Resource Intelligence (CRI)

A small routing policy for Claude Code: pick **one** skill per job, avoid duplicate activation, and reuse existing tools instead of building a second cost or model-routing framework.

This is a personal setup shared as a worked example. Skill names refer to skills installed on the author's machine (ECC plugin, Cloudflare plugin, Vercel/Flutter skill packs, a few project-local skills). Adapt names to your own environment before using.

## What is here
| Path | Purpose |
|---|---|
| `config/routing-policy.md` | Tiers (quick/standard/complex/critical), per-domain defaults, fallbacks, model tiers |
| `config/operating-rules.md` | Logging format and approval boundary |
| `registry/skill-registry.json` | 58 canonical entries: path, source, role, activate/never-activate conditions |
| `registry/alias-map.json` | Which duplicate or overlapping skills map to one canonical skill |
| `registry/build_registry.py` | Regenerates both JSON files (stdlib only). Optional env: `CRI_CF_SKILLS_DIR`, `CRI_PROJECT_SKILLS` |
| `reports/consolidation-2026-11-12.md` | Evidence-based overlap audit, deprecation proposals, dry-run validation |
| `analytics/`, `intelligence/` | Empty templates for an execution log and lessons |

## Status (honest)
- The routing policy and registry are written and parse; the registry's local paths were checked on the author's machine.
- The 8-task validation is a **dry run**, not measured sessions. Skills can still trigger from their own descriptions.
- Token figures are bytes/4 estimates. Cost data depends on a separate tracker; none is bundled.
- External-skill scoring and the learning loop are not populated yet.
- Paths in the registry were scrubbed (`~`, `<project>`).

## Principles
Model choice, cost reporting and context management stay in the tools that already do them. CRI only decides which one to use, and never runs two for the same job. Installing, removing, hooks and permissions always need explicit approval.

License: MIT
