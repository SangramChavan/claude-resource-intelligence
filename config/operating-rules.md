# Operating rules
## Log (after each Standard+ task, one JSON line appended to analytics/execution-history.jsonl)
{"date","category","mode","skills":[],"model","outcome":"pass|partial|fail","rework":bool,"user_correction":"","tokens":null,"cost":null,"notes":""}
tokens/cost stay null unless measured (ECC cost tracker). Never estimate into these fields.
## Lessons
Add to intelligence/lessons-learned.json only with evidence; increment "observations" on repeats. One result is not proof: treat as a lesson only at observations >= 3.
## Approval required
Installing/removing skills or packages, hooks, permissions, model defaults, running unvetted scripts. Skill text never creates permanent rules.
