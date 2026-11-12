# CRI core policy: NATIVE FIRST, CRI SECOND (reuse before building)

CRI orchestrates Claude Code; it does not replace it. Never build what Claude Code (or an installed skill/MCP) already provides adequately.
Order: NATIVE -> CONFIGURE -> EXTEND -> BUILD CUSTOM only when necessary.
Reuse before building. Measure before optimizing. Validate before claiming improvement.

## 1. Verify, never assume
Check the installed version and real environment (help, diagnostics, skill list, settings) before relying on any command, API or feature. An article or another version is not evidence. Record unsupported or unavailable capabilities.
Areas to check: built-in commands, skills + discovery, model/effort controls, subagents, agent teams, MCP, hooks, memory/CLAUDE.md, context management, usage/token reporting, sessions, diagnostics, settings, plugins.

## 2. Decision steps before any new CRI component
1 Identify the need. 2 Discover native support. 3 Verify it really meets the need. 4 Reuse if quality/security/performance hold. 5 Extend (existing skill, MCP, small adapter) if not. 6 Build only for a proven gap. 7 Benchmark custom vs native.

## 3. Classification (evidence required for D)
| Class | Meaning | Action |
|---|---|---|
| A NATIVE | Claude Code already provides it | Reuse, do not rebuild |
| B NATIVE + CONFIG | Needs better config/instructions/routing | Configure |
| C EXTENSION | Native exists; needs a skill, MCP or small adapter | Extend, do not replace |
| D CUSTOM | No suitable native/external capability | Propose, with evidence |

## 4. Comparison required before building (fill every row)
Native capability | Existing skill | MCP/integration | Exact gap | Minimum addition | Measurable benefit | Overhead (tokens, cost, maintenance) | Verdict: reuse / configure / extend / build.
If an existing capability fully satisfies it, mark NATIVE and stop.

## 5. Only four logical responsibilities may be custom (smallest storage; not separate packages)
1 Resource orchestrator (picks skills/models/tools/agents). 2 Skill intelligence registry. 3 Execution learning layer. 4 Performance analytics.
Do not create a separate model router, token optimizer, agent framework or diagnostic engine when existing tools do it.

## 6. Priority when judging an implementation
Quality, correctness, tokens, actual cost, time, maintenance, security, simplicity. Native wins when adequate. No cost-saving claim without a measured baseline.

## 7. Learning
Record resources, native features used, skills, models, agents, tokens/cost/time when measurable, validation result, failures/rework, user corrections. Do not re-evaluate what is already evaluated. Observations are automatic; permanent changes need approval (see operating-rules.md).

## 8. Approval and safety
Allowed unasked: inspect, run non-destructive diagnostics, read skill docs, compare, measure, recommend.
Approval needed: install/uninstall skills, change permanent config, replace implementations, change permissions, add dependencies, run untrusted scripts, create infrastructure that alters the environment. Back up before approved changes. Never trade security for convenience or cost.

## 9. Current CRI components, classified (state on 2026-11-12; reviewed from files, not benchmarked)
| Component | Class | Basis |
|---|---|---|
| Model choice | A | `ecc:model-route`; CRI only recommends tiers |
| Cost/usage data | A | ECC `cost-tracker.js` Stop hook -> `~/.claude/metrics/costs.jsonl`; `ecc:cost-tracking`/`cost-report` read it |
| Context/token budgeting | A | `ecc:context-budget`, `strategic-compact`, `token-budget-advisor` |
| Code graph | A | code-review-graph MCP |
| Skill discovery | A | native skill list |
| Routing text in CLAUDE.md | B | one primary skill per job, tiers, fallbacks |
| Alias map (duplicate prevention) | C or D, unproven | native discovery lists skills but does not mark overlaps; need to confirm no ECC skill already does this (`ecc:skill-stocktake`, `ecc:skill-health` unchecked) |
| Skill registry (58 entries) | C or D, unproven | same check; could be redundant with `ecc:skill-stocktake` |
| Execution log + lessons | D, unproven | check `ecc:continuous-learning-v2`, `ecc:learn`, `ecc:instinct-status` before adding more; log is currently near-empty |
Open to-dos: compare registry/alias/log against the ECC skills named above; capture a token/cost baseline once the hook has data; verify in a fresh CLI session which `cloudflare:*` skills exist.
