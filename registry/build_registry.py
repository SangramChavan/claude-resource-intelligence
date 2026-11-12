#!/usr/bin/env python3
"""Regenerates skill-registry.json and alias-map.json from the spec below.
Edit SPEC, run: python3 -I build_registry.py   (stdlib only)"""
import json, os
H = os.path.expanduser("~")
E = H + "/.claude/plugins/cache/ecc/ecc/2.2.3"
CF = "plugin:cloudflare@1.0.4 (synced desktop plugin, repo cloudflare/skills)"
VERIFIED = "2026-11-12"
SEC = "frontmatter+headings read; bodies not scanned for scripts/network calls"

def e(name, path, cap, resp, act, excl, dup=None, src=None, ver=None, deps=None, sec=SEC, role="specialist"):
    return dict(canonical=name, path=path, source=src, version=ver, category=cap, role=role,
                responsibility=resp, dependencies=deps or [], duplicates=dup or [],
                activate_when=act, never_activate_when=excl, security_status=sec, last_verified=VERIFIED)

P = os.path.expanduser(os.environ.get("CRI_PROJECT_SKILLS", "~/Documents/Claud/.claude/skills"))  # project-local skills (explore-codebase)
G = H + "/.claude/skills"
ECC = "ecc@2.2.3 (affaan-m/ECC)"
S = []
# ---- UI design ----
S += [
 e("design-taste-frontend", G+"/design-taste-frontend", "ui-design", "Primary web UI: brief inference, design dials, official design-system mapping, anti-slop pre-flight (87KB ~22k tok)",
   "New or redesigned website, landing page, portfolio, marketing site", "Dashboards/forms/multi-step product flows (use ui-ux-taste); native Apple apps; one-line copy tweaks",
   dup=["ecc:frontend-design-direction"], src="global (moved from project 2026-11-12; unknown upstream)", role="primary-ui-web"),
 e("ui-ux-taste", G+"/ui-ux-taste", "ui-design", "Primary for product UI: dashboards, forms, flows; reduction of complexity (6.5KB ~1.6k tok)",
   "App/dashboard/form/flow UI, simplify or review an interface", "Marketing/landing pages (design-taste-frontend)", src="global (moved from project 2026-11-12)", role="primary-ui-app"),
 e("ecc:design-system", E+"/skills/design-system", "design-system", "Optional: extract tokens from existing codebase, DESIGN.md, 10-dim audit, AI-slop flags (2.8KB)",
   "Need design tokens/DESIGN.md or visual-consistency audit", "Single landing page with no system requirement", dup=["design-system"], src=ECC, ver="2.2.3", role="design-system-specialist"),
 e("design-system", G+"/design-system", "design-system", "Fallback: 3-layer token architecture + slide token pipeline. Lists agents that may not exist (ui-ux-designer, frontend-developer)",
   "Only when slides/brand pipeline needs token files", "Any normal web UI task (ecc:design-system is canonical)", dup=["ecc:design-system"], src="nextlevelbuilder family (unverified repo)", role="fallback"),
 e("ui-ux-pro-max", G+"/ui-ux-pro-max", "ui-design", "Optional visual-design data lookup: searchable styles/palettes/fonts (55KB ~14k tok). Global copy differs from plugin 2.13.0 copy",
   "Explicit request for palette/font/style options backed by data, or stack-specific UI rules", "Default web UI work (loads 14k tokens for little gain)", dup=["ui-ux-pro-max@plugin 2.13.0"], src="nextlevelbuilder/ui-ux-pro-max-skill", ver="global copy unversioned; plugin 2.13.0", deps=["python3"], role="visual-specialist"),
 e("ui-styling", G+"/ui-styling", "ui-implementation", "Support: shadcn/ui + Radix + Tailwind implementation patterns",
   "Stack is shadcn/Tailwind and components must be built", "Other stacks (Material, Carbon, Fluent); pure design direction", src="nextlevelbuilder family", role="support"),
 e("apple-design", G+"/apple-design", "ui-design", "Apple HIG reviewer/improver for iOS/macOS/Flutter/RN/Tauri/Electron",
   "Native Apple platform UI, explicit HIG/Apple-style request, UI review of mobile/desktop app screenshots", "Ordinary web projects unless user asks for an Apple-like look", src="dickwu/apple-design-skill", role="apple-specialist"),
 e("brand", G+"/brand", "branding", "Brand voice, identity, guidelines, token sync", "Brand guidelines/voice/messaging work", "Building UI", dup=[], src="nextlevelbuilder family", role="brand-specialist"),
 e("banner-design", G+"/banner-design", "banner", "Banners/ad/social/hero creative with multiple art directions", "Banner, cover, ad creative", "Website UI", dup=["design (banner sub-route)"], src="nextlevelbuilder family", role="banner-specialist"),
 e("slides", G+"/slides", "presentation", "Strategic HTML decks (Chart.js, tokens)", "Presentation/pitch deck as HTML", "Websites", dup=["design (slides sub-route)", "ecc:frontend-slides"], src="nextlevelbuilder family", role="slides-specialist"),
 e("design", G+"/design", "branding-assets", "Umbrella router; keep ONLY for logo, CIP mockups, icons, social photos (its other routes duplicate specialists)",
   "Logo, corporate identity program, SVG icons, social photos", "Banner/slides/brand/tokens/UI (route to the specialist directly)", dup=["brand", "banner-design", "slides", "design-system", "ui-styling"], src="nextlevelbuilder family", deps=["Gemini API key (logo/icon)"], role="asset-specialist"),
]
# ---- Cloudflare ----
cf = [("cloudflare","product choice/architecture on Cloudflare; routes to other CF skills"),
 ("wrangler","Wrangler CLI for wrangler.* projects"),("cf-cli","cf CLI (beta) for new projects/API"),
 ("workers-best-practices","Workers production config and code review"),("workers-development","local dev, Local Explorer, traces (NEW, no bare copy)"),
 ("durable-objects","Durable Objects"),("web-perf","web performance/CWV audit"),("workers-profiling","CPU/memory profiling"),
 ("frameworks-on-cloudflare","framework apps on Workers (NEW)"),("cloudflare-app-bootstrap","bindings/secrets/local run (NEW)"),
 ("nextjs-on-cloudflare","Next.js via vinext"),("turnstile-spin","Turnstile"),("cloudflare-email-service","Email sending/routing"),
 ("agents-sdk","Agents SDK"),("cloudflare-one","Zero Trust/SASE")]
for n, r in cf:
    S.append(e("cloudflare:"+n, "plugin:cloudflare/skills/"+n, "cloudflare", r, "Task is on Cloudflare services", "Non-Cloudflare hosting; never load bare '"+n+"' alongside",
               dup=[G+"/"+n+" (older snapshot, 2026-10-25)"] if n not in ("workers-development","frameworks-on-cloudflare","cloudflare-app-bootstrap") else [],
               src=CF, ver="1.0.4", deps=["cloudflare MCP needs OAuth for live API"], role="canonical"))
# ---- Security ----
S += [
 e("security-audit", H+"/.agents/skills/security-audit", "security", "DEFAULT security workflow: guidance mode by default, six-phase audit only on explicit request",
   "Auth, payments, input handling, APIs, secrets; explicit audit/pen-test", "Typos, docs, styling-only changes", dup=["ecc:security-review", "engineering/security checks in code-review"], src="cloudflare/security-audit-skill", role="default"),
 e("ecc:security-scan", E+"/skills/security-scan", "security-scanner", "AgentShield scan of .claude config, hooks, MCP, permissions, secrets (different surface from app code)",
   "Changing hooks/MCP/permissions/agent config, or before sharing a .claude directory", "Application source review", src=ECC, ver="2.2.3", deps=["npx ecc-agentshield (needs approval to run)"], role="independent-scanner"),
 e("ecc:security-bounty-hunter", E+"/skills/security-bounty-hunter", "security", "Remote-reachable exploit hunting for bounty-style reports", "Explicit bounty/exploitability hunt", "Routine reviews", src=ECC, ver="2.2.3", role="specialist"),
 e("ecc:agent-security-hardening", E+"/skills/agent-security-hardening", "security", "Hardening for AI agent runtimes/tool gateways", "Building an agent runtime", "Ordinary web apps", src=ECC, ver="2.2.3", role="specialist"),
 e("ecc:security-reviewer (agent)", E+"/agents/security-reviewer.md", "security-validation", "Independent second reviewer on Sonnet for critical production changes", "Critical change after security-audit pass", "Routine changes", src=ECC, ver="2.2.3", role="independent-validation"),
]
# ---- Code review ----
S += [
 e("code-review", "built-in skill (not on disk)", "code-review", "DEFAULT reviewer: diff/PR, effort levels, optional --fix", "Review of a diff, branch or PR", "Trivial edits", dup=["engineering:code-review", "ecc:code-review"], src="Claude Code built-in", role="default"),
 e("review-changes", G+"/review-changes", "code-review", "Graph-based change/impact review (1.3KB); uses code-review-graph MCP", "Small-to-medium change in a repo whose graph is built, as a cheaper substitute for code-review", "Repos without .code-review-graph or without the MCP configured", deps=["code-review-graph MCP (configured per project in .mcp.json)"], src="global (moved from project 2026-11-12)", role="change-specific"),
 e("ponytail-review", H+"/.claude/plugins/cache/ponytail/ponytail/4.10.0/.openclaw/skills/ponytail-review", "code-review", "Over-engineering finder only (different dimension)", "Asked to find code to delete", "Correctness review", src="DietrichGebert/ponytail", ver="4.10.0", role="specialist"),
 e("simplify", "built-in skill (not on disk)", "refactor", "Applies simplification fixes (not a reviewer)", "After a change, to clean it up", "Bug hunting", src="Claude Code built-in", role="simplifier"),
 e("ecc:review-pr", E+"/commands/review-pr.md", "code-review", "Multi-agent PR pass (6 agents)", "Critical PR needing second independent review", "Routine changes (costly)", src=ECC, ver="2.2.3", role="critical-second-reviewer"),
]
# ---- Codebase knowledge ----
S += [
 e("code-review-graph (MCP)", "mcp: code-review-graph", "codebase-graph", "Primary graph: AST call/import/test edges, impact radius, auto-updated by hook, queryable", "Any code-relationship question, impact analysis, review context", "Pure-text search (use rg)", deps=["git repo for auto-update hook"], src="MCP server", role="primary-graph"),
 e("graphify", G+"/graphify", "codebase-graph", "Multimodal graph (code+docs+images+video), report with god nodes (41KB ~10k tok)", "Mixed corpus (docs/papers/media), or graphify-out/ already exists and question is conceptual", "Code-only questions when code-review-graph exists; never rebuild when graphify-out/ exists", src="graphify (unverified repo)", role="secondary-graph"),
 e("explore-codebase", P+"/explore-codebase", "codebase-exploration", "Thin wrapper over code-review-graph for orientation (1.3KB)", "First look at an unfamiliar repo with graph built", "Repo has no graph", deps=["code-review-graph MCP"], src="project-local", role="exploration"),
 e("ecc:codebase-onboarding", E+"/skills/codebase-onboarding", "onboarding", "Writes onboarding guide + starter CLAUDE.md (writes files)", "Joining a repo that has no CLAUDE.md, or explicit onboarding doc request", "Quick questions", src=ECC, ver="2.2.3", role="onboarding"),
]
# ---- Planning ----
S += [
 e("grill-me", G+"/grill-me", "planning-clarify", "One-question-at-a-time requirement interrogation", "Requirements unclear or plan needs stress test", "Clear tasks", src="unverified", role="clarify"),
 e("ecc:plan", E+"/commands/plan.md", "planning", "DEFAULT plan: restate, risks, steps, waits for confirmation", "Standard feature/refactor needing a plan", "Small edits", dup=["ecc:prp-plan"], src=ECC, ver="2.2.3", role="default"),
 e("ecc:plan-prd", E+"/commands/plan-prd.md", "planning", "Lean PRD then hands to ecc:plan", "Product-level scoping", "Engineering tasks", src=ECC, ver="2.2.3", role="specialist"),
 e("engineering:system-design", "plugin:engineering/skills/system-design", "architecture", "System design framework", "Designing a product architecture", "Single-feature work", src="synced engineering plugin", role="architecture"),
 e("engineering:architecture", "plugin:engineering/skills/architecture", "architecture", "ADR for technology choices / alternatives", "Comparing technology options", "Routine work", src="synced engineering plugin", role="alternatives"),
 e("ecc:blueprint", E+"/skills/blueprint", "planning", "Multi-session, multi-agent construction plan", "Large multi-PR project", "Single-session work", src=ECC, ver="2.2.3", role="large-plan"),
 e("ecc:prp-plan", E+"/commands/prp-plan.md", "planning", "Feature plan with codebase pattern extraction", "Never by default (overlaps ecc:plan)", "Always", dup=["ecc:plan"], src=ECC, ver="2.2.3", role="alias"),
 e("ecc:multi-plan", E+"/commands/multi-plan.md", "planning", "Dual-model plan; REQUIRES external ccg-workflow runtime (not installed)", "Only if runtime installed AND user asks for dual-model drafts", "Always otherwise", deps=["ccg-workflow runtime (absent)"], src=ECC, ver="2.2.3", role="unavailable"),
 e("ecc:plan-orchestrate", E+"/skills/plan-orchestrate", "planning", "Turns an existing plan doc into ECC slash commands (generative only)", "A plan document exists and user wants step commands", "No plan doc", src=ECC, ver="2.2.3", role="specialist"),
]
# ---- Cost / model ----
S += [
 e("ecc:model-route", E+"/commands/model-route.md", "model-routing", "Recommend model tier by complexity/risk/budget (697B)", "Non-trivial task where model choice matters", "Quick tasks", src=ECC, ver="2.2.3", role="canonical-router"),
 e("ecc:cost-tracking", E+"/skills/cost-tracking", "cost-reporting", "Spend/usage from ~/.claude/metrics/costs.jsonl (written by a narrow Stop hook since 2026-11-12; other ECC hooks stay off)", "User asks about spend", "Trivial tasks", deps=["cost-tracker Stop hook in settings.json (path pinned to ecc 2.2.3)"], src=ECC, ver="2.2.3", role="reporting"),
 e("ecc:cost-report", E+"/commands/cost-report.md", "cost-reporting", "Terminal/CSV report from same log", "User asks for report AND log exists", "Trivial tasks", deps=["cost-tracker Stop hook in settings.json (path pinned to ecc 2.2.3)"], src=ECC, ver="2.2.3", role="reporting"),
 e("ecc:context-budget", E+"/skills/context-budget", "context", "Routes to native context meter; static audit only on request", "Context capacity questions", "Normal tasks", src=ECC, ver="2.2.3", role="context"),
 e("ecc:strategic-compact", E+"/skills/strategic-compact", "context", "Compaction timing", "Long session near limit", "Short sessions", src=ECC, ver="2.2.3", role="context"),
 e("ecc:token-budget-advisor", E+"/skills/token-budget-advisor", "budget", "Response-depth choice (25/50/75/100%)", "User asks for a short/long answer choice", "Default", src=ECC, ver="2.2.3", role="budget"),
 e("ecc:cost-aware-llm-pipeline", E+"/skills/cost-aware-llm-pipeline", "cost-execution", "Routing/caching patterns when BUILDING LLM apps", "Building an app that calls LLM APIs", "Using Claude Code itself", src=ECC, ver="2.2.3", role="app-dev"),
 e("ecc:prompt-caching-strategy", E+"/skills/prompt-caching-strategy", "cost-execution", "Prompt caching design for LLM apps", "Building LLM apps", "Normal coding", src=ECC, ver="2.2.3", role="app-dev"),
 e("ecc:token-card", E+"/skills/token-card", "visualization", "Commits a usage card file to a repo", "Explicit request only", "Always otherwise", src=ECC, ver="2.2.3", role="visualization"),
]
reg = dict(schema=1, generated=VERIFIED, note="Descriptions/headings read directly; security_status means no script audit yet. Token figures elsewhere are bytes/4 estimates.", skills=S)
CFDIR = os.environ.get("CRI_CF_SKILLS_DIR", H + "/.claude/plugins/cache/cloudflare/cloudflare/1.0.4/skills")  # cloudflare plugin skills dir
# derived from directories present in both places, not hand-listed
bare_cf = sorted(set(os.listdir(G)) & set(os.listdir(CFDIR))) if CFDIR and os.path.isdir(CFDIR) else []
print("cloudflare twins:", len(bare_cf), "from", CFDIR)
alias = {
 "ui_design_web": dict(canonical="design-taste-frontend", aliases=["ecc:frontend-design-direction", "ui-ux-pro-max (default use)", "design (UI route)"]),
 "ui_design_app": dict(canonical="ui-ux-taste", aliases=[]),
 "design_system": dict(canonical="ecc:design-system", aliases=["design-system"]),
 "ui_implementation": dict(canonical="ui-styling", aliases=[], note="support only when shadcn/Tailwind"),
 "banner": dict(canonical="banner-design", aliases=["design (banner route)"]),
 "slides": dict(canonical="slides", aliases=["design (slides route)", "ecc:frontend-slides"]),
 "cloudflare": dict(canonical_prefix="cloudflare:", bare_to_namespaced={n: "cloudflare:"+n for n in bare_cf}, rule="Never activate bare and namespaced of the same name; bare dir is the 2026-10-25 snapshot, namespaced is v1.0.4 (2026-11-08)"),
 "security_default": dict(canonical="security-audit", aliases=["ecc:security-review", "security-review (checklist use)", "ecc:security-reviewer (as default)"]),
 "code_review": dict(canonical="code-review", aliases=["engineering:code-review", "ecc:code-review"]),
 "planning_standard": dict(canonical="ecc:plan", aliases=["ecc:prp-plan"]),
 "model_routing": dict(canonical="ecc:model-route", aliases=["ecc:cost-aware-llm-pipeline (apps only)"]),
 "codebase_graph": dict(canonical="code-review-graph (MCP)", aliases=[], secondary="graphify (non-code corpora)"),
 "not_ui": dict(note="ecc:taste, ecc:taste-application, ecc:taste-distillation are VIDEO skills (angelcore music video / LUT style packs). Never match for UI taste requests."),
}
def scrub(o):  # write portable paths: home dir becomes ~
    if isinstance(o, dict): return {k: scrub(v) for k, v in o.items()}
    if isinstance(o, list): return [scrub(v) for v in o]
    return o.replace(H, "~") if isinstance(o, str) else o
reg, alias = scrub(reg), scrub(alias)
base = os.path.dirname(os.path.abspath(__file__))
json.dump(reg, open(base + "/skill-registry.json", "w"), indent=1)
json.dump(alias, open(base + "/alias-map.json", "w"), indent=1)
print(len(S), "entries;", len(bare_cf), "cloudflare aliases")
