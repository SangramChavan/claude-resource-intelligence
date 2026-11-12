# CRI routing policy (orchestration only)

CRI selects; it does not re-implement. Model choice = `ecc:model-route`. Cost data = ECC cost-tracking (needs `~/.claude/metrics/costs.jsonl`). Context = `ecc:context-budget`.

## Tiers
| Tier | Rule |
|---|---|
| Quick | No skill, no announcement. Cheapest capable model. |
| Standard | One primary skill + at most one support skill for a distinct job. Say "Skill: X". |
| Complex | One primary skill per distinct responsibility. Independent validation only if it checks something different. |
| Critical | Primary + one independent reviewer/scanner. Strongest justified model. |

A skill that already covers a subtask serves it; do not add another. Look up `alias-map.json` before activating: if a candidate is an alias of one already active, skip it.

## Availability fallbacks (inferred from installed_plugins.json, not verified in a CLI session)
| Default | Fallback if not in the session's skill list |
|---|---|
| cloudflare:* | bare Cloudflare skill of the same name |
| design-taste-frontend / ui-ux-taste | ecc:frontend-design-direction |
| review-changes | code-review |
| engineering:* | ecc:plan / ecc:blueprint |

## Per-domain defaults
| Job | Default | Add only when | Never |
|---|---|---|---|
| Web UI (marketing/landing/redesign) | design-taste-frontend | shadcn/Tailwind build: ui-styling; tokens/audit: ecc:design-system; data-backed palette/fonts: ui-ux-pro-max | apple-design, design, ecc:frontend-design-direction together |
| App UI (dashboard/form/flow) | ui-ux-taste | same adds | design-taste-frontend simultaneously |
| Apple / native UI, HIG review | apple-design | ecc:liquid-glass-design (iOS 26 code) | for ordinary web |
| Brand / banner / slides / logo | brand / banner-design / slides / design (logo, CIP, icons) | | design for banner/slides/brand |
| Cloudflare | cloudflare:* (route via `cloudflare:cloudflare`) | task-specific sibling (workers-development, durable-objects...) | bare copies in ~/.claude/skills |
| Security | security-audit (guidance) | full audit on explicit request; ecc:security-scan for hooks/MCP/permissions; ecc:security-reviewer agent as 2nd reviewer on critical | ecc:security-review alongside security-audit |
| Dependency vulns | `npm audit` / osv-scanner (no skill covers it; osv-scanner not installed) | | |
| Code review | code-review | review-changes if graph built (cheaper); ecc:review-pr or 2nd agent on critical; ponytail-review to find deletions; simplify to apply cleanups | engineering:code-review, ecc:code-review |
| Codebase knowledge | code-review-graph MCP | graphify for docs/media corpora or existing graphify-out; explore-codebase for orientation; ecc:codebase-onboarding when documenting | building both indexes; rebuilding an existing one |
| Planning | unclear: grill-me; standard: ecc:plan | PRD: ecc:plan-prd; architecture: engineering:system-design + engineering:architecture; multi-session: ecc:blueprint; plan doc to commands: ecc:plan-orchestrate | ecc:prp-plan with ecc:plan; ecc:multi-plan (runtime absent) |
| Model / cost | ecc:model-route (non-trivial only) | context-budget for capacity; cost-tracking/cost-report on request AND log exists | token reports on trivial tasks; cost-aware-llm-pipeline unless building an LLM app |

## Model tiers (names from current environment; pricing and entitlement NOT verified)
L1 Haiku 5.5 (exploration, formatting) / L2 Sonnet 5.5 (default build) / L3 Opus 5.5 (architecture, security audit, critical review) / L4 Fable 5.1 (only with an identified capability gap). Recommend, never auto-switch defaults.
