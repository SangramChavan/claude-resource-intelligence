# Skill consolidation report (2026-11-12)

Method: frontmatter, headings and diffs read from disk. Skill bodies were not scanned for scripts. Token figures = file bytes / 4 (estimates). Validation below is a policy dry-run, not executed task runs.

## 1. Overlap audit: key findings
- **Cloudflare**: the namespaced `cloudflare:*` set is the plugin `cloudflare` v1.0.4 (repo cloudflare/skills, synced desktop plugin, files dated 2026-11-08). The bare `~/.claude/skills` copies are an older snapshot (2026-10-25) of the same repo. Of 22 namespaced skills, 19 have a bare twin: all differ (4 to 69 diff lines); the changes are newer content (placement guidance, CPU-limit wording, observability/traces, `cf` CLI preference, skill-feedback section). Three are namespaced-only: `workers-development`, `frameworks-on-cloudflare`, `cloudflare-app-bootstrap`. Verdict: **updated versions, not different implementations**. Canonical = namespaced. D1, KV, R2, Queues, Hyperdrive etc. live in `cloudflare/references/*`, so no separate skills are needed.
- **UI**: `design` is an umbrella router over brand, design-system, ui-styling, banner, slides (same nextlevelbuilder family), plus built-in logo/CIP/icon/social-photo. `design-system` lists dependency agents (ui-ux-designer, frontend-developer) that are not installed. `ecc:taste`, `ecc:taste-application`, `ecc:taste-distillation` are **video** skills, not UI taste (false overlap). `design-taste-frontend` (87KB) covers web direction and itself says dashboards/forms belong to `ui-ux-taste`. Global `ui-ux-pro-max` differs from the plugin 2.13.0 copy.
- **Security**: `security-audit` (cloudflare/security-audit-skill, 22KB) is the full workflow. `ecc:security-review` is a generic checklist (overlap). `ecc:security-scan` runs AgentShield on agent config/hooks/MCP/permissions, a different detection surface (keep). No installed skill covers dependency vulnerabilities (gap).
- **Code review**: `code-review` (built-in, effort levels), `engineering:code-review` (security/perf/correctness, duplicate), `ecc:code-review` (PRP checklist, duplicate), `review-changes` (graph-based, 1.3KB), `ponytail-review` (over-engineering only, different dimension), `simplify` (applies fixes, not a reviewer), `ecc:review-pr` (6-agent pass, critical only).
- **Codebase**: code-review-graph MCP = AST call/import/test graph with auto-update hook. graphify = multimodal corpus graph + report. Complementary for mixed corpora, competing for code-only. `explore-codebase`/`review-changes` are thin wrappers over the MCP.
- **Planning**: `ecc:plan` (confirm gate), `ecc:prp-plan` (overlaps), `ecc:plan-prd`, `ecc:blueprint` (multi-session), `ecc:plan-orchestrate` (turns a plan doc into commands), `grill-me` (clarify), `engineering:system-design`/`architecture` (architecture/ADR). `ecc:multi-plan` needs the external ccg-workflow runtime, which is not installed.
- **Cost/model**: `ecc:model-route` (697B heuristic) is the only router. `ecc:cost-tracking`/`cost-report` read `~/.claude/metrics/costs.jsonl`, which **does not exist** because ECC hooks are disabled (`hooks_enabled:false`), so they would report nothing. `context-budget`, `strategic-compact`, `token-budget-advisor`, `token-card`, `cost-aware-llm-pipeline`, `prompt-caching-strategy` each have a narrow trigger.

## 2. Canonical selection
See `registry/alias-map.json` (machine form) and `config/routing-policy.md` (rules).

## 3. Proposed deprecations (NOT executed, need approval)
| Item | Why | Risk |
|---|---|---|
| Bare Cloudflare skills in `~/.claude/skills` (19 dirs: agents-sdk, basin, cf-cli, cloudflare, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, durable-objects, gateway-workers, k2, nextjs-on-cloudflare, sandbox-migrate-to-next, sandbox-next, sandbox-stable, turnstile-spin, web-perf, workers-best-practices, workers-profiling, wrangler) | Older snapshot of namespaced plugin | Namespaced plugin lives in the desktop app session store; CLI-only use might lose it. Verify the CLI sees `cloudflare:*` first |
| `ecc:security-review` as default | Alias of security-audit guidance | None |
| `ecc:prp-plan`, `ecc:code-review`, `engineering:code-review` | Aliases | None |
| `design-system` (global) | Alias of `ecc:design-system` except slide-token pipeline | Low |
| `ecc:multi-plan` | Runtime absent | None |
| 10 real-dir copies (hyperframes*, media-use, reverse-engineer-anything) in `~/.claude/skills` | Byte-identical to `~/.agents` | Replace with symlinks |
| Instagram/YouTube/Flutter groups (about 52 skills) | Conditional domains | Disable per project instead of deleting |
Also recommended (approval): promote `design-taste-frontend` and `ui-ux-taste` from this project to global, because they only exist under `<project>/.claude/skills`; enable the ECC cost-tracker hook so cost skills have data.

## 4. ECC functionality reused (nothing duplicated)
Model selection `ecc:model-route`; cost data `ecc:cost-tracking`/`cost-report` (pending hook); context `ecc:context-budget`, `strategic-compact`; planning `ecc:plan`, `blueprint`; scan `ecc:security-scan`; second reviewers `ecc:review-pr`, `ecc:security-reviewer`; onboarding `ecc:codebase-onboarding`; design system `ecc:design-system`. CRI adds only: registry, alias map, routing policy.

## 5. Before vs after (rule-derived, not measured)
| Scenario | Before (CLAUDE.md said) | After |
|---|---|---|
| Any task | Scan list, name top 3 skills, even if small | Quick: none |
| Any UI task | apple-design ("when building or changing UI", about 6.2k tok) | design-taste-frontend or ui-ux-taste; apple-design only if Apple-native |
| Frontend page | web-perf (bare) + possible cloudflare:web-perf both match | cloudflare:web-perf only on perf request |
| Code-relationship question | graphify first if graphify-out exists, plus code-review-graph from project CLAUDE.md | code-review-graph; graphify only for docs/media |
| Every project prompt | karpathy + superpowers (not installed) + skill-creator | karpathy on non-trivial code; skill-creator on skill work |
Always-loaded global CLAUDE.md size went from 3,514 to 4,383 bytes: about +0.2k tokens per session, traded for removing multi-thousand-token duplicate activations. Savings per task depend on use and were not measured.

## 6. Validation (dry-run of routing)
| # | Task | Skills selected | Deliberately excluded | Model | Est. skill tokens | Dependencies | Validation |
|---|---|---|---|---|---|---|---|
| 1 | Modern SaaS website | design-taste-frontend (21.8k); ui-styling (2.5k) only if shadcn | apple-design, ui-ux-pro-max, design, ecc:frontend-design-direction, ui-ux-taste | L2 Sonnet | about 22-25k | open-seo checklist (existing rule) | Playwright screenshots mobile+desktop; Lighthouse |
| 2 | Workers + D1 app | cloudflare:cloudflare (6.8k) then workers-best-practices (1.4k), wrangler or cf-cli (2.9k) | bare CF copies, durable-objects, nextjs-on-cloudflare | L2 Sonnet | about 11k | Cloudflare account/OAuth for live deploy | wrangler dev + real request; workers-development Local Explorer |
| 3 | Production code review | code-review; security-audit guidance if sensitive; critical: + ecc:review-pr or security-reviewer agent | ecc:code-review, engineering:code-review, ponytail-review, simplify | L3 Opus | about 6k (+agents) | none | cited findings with file:line; second pass on critical |
| 4 | Security audit | security-audit (full, 5.5k+refs) | ecc:security-review; ecc:security-scan unless .claude config in scope | L3 Opus | about 6-10k | write access for artifacts; npm audit for deps (osv-scanner absent) | Evidence per finding; independent ecc:security-reviewer if production-critical |
| 5 | Explore unfamiliar repo | code-review-graph MCP + explore-codebase (0.3k) | graphify, codebase-onboarding unless asked | L1 Haiku or Explore agent | under 1k | git repo for graph hooks | Answers cite files; no new index if one exists |
| 6 | Full product architecture | grill-me if unclear (0.6k); engineering:system-design (0.3k); architecture ADR (0.6k); ecc:blueprint if multi-session (1.3k) | ecc:plan/prp-plan, multi-plan | L3 Opus + advisor | about 3k | none | ADR with options and trade-offs; advisor review |
| 7 | Estimate/optimize token cost | ecc:model-route (0.2k); ecc:context-budget (1.6k) | cost-tracking/cost-report (no log), token-card, cost-aware-llm-pipeline unless building an LLM app | L2 Sonnet | about 2k | ECC cost hook is OFF, so no real spend data; estimates only | Label results as estimates until hook enabled |
| 8 | Brand identity + banner | brand (0.7k); design for logo (3.1k); banner-design (2.1k) | design-taste-frontend, apple-design, slides | L2 Sonnet | about 6k | Gemini API key for logo/banner generation (unverified) | Visual review of outputs at target sizes |

Duplicate activation after the change: **none in the 8 dry runs**. Caveat: skills still auto-trigger from their own descriptions (for example `apple-design` and `ui-ux-taste` descriptions are broad). The routing text reduces this but cannot block it; the real test is observing a few live sessions.

## 7. Not done / needs approval
No skill, package or MCP server was deleted, uninstalled or replaced. No settings or permissions changed. Backups: `~/.claude/backups/CLAUDE.md.2026-11-12.pre-cri.bak` and `Claud-CLAUDE.md.2026-11-12.pre-cri.bak`.

## Update (2026-11-12, after setup)
- `design-taste-frontend`, `ui-ux-taste` and `review-changes` were moved from the project to `~/.claude/skills` (global). `review-changes` still needs the code-review-graph MCP, which is configured per project.
- Cost data now exists: `~/.claude/metrics/costs.jsonl` is written by a single ECC `cost-tracker.js` Stop hook. ECC `hooks_enabled` remains false, so `skill-health` and `continuous-learning-v2` still have no hook data. The hook path is pinned to `ecc/2.2.3`.
- Statements above that the cost file does not exist describe the state at audit time.
