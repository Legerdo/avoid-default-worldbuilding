# Behavioral regression cases

`cases.json` contains predeclared prompts and observable requirements. These are
semantic acceptance cases, **not automatically executed model benchmarks**.
`candidate_fixture` is an intentionally authored example, not a measured output.
`must` and `must_not` belong to the reviewer and must not be shown to the generator.

## Run a case

1. Freeze the skill version/hash and the case file hash. Start a clean session.
2. Activate the installed skill. To test instructions separately, inject SKILL.md
   into a fresh context and record `instruction-injection`, not `native-activation`.
3. Replay `prior_turns`, when present, then send only `prompt` to the generator.
   The prompt itself already contains a draft when needed; do not append fixtures.
4. Save the exact visible output and observed host/model/settings. Missing model
   metadata must remain `unknown`. Do not report an assumed model as observed.
5. A different reviewer checks every `must` and `must_not`, including semantic
   equivalents, preservation of permissions and requested format. Record PASS,
   FAIL or UNRESOLVED with short output evidence. Model self-reports do not count.

## What each category protects

- `blocked-central`: replace an unwanted central setup, not just its vocabulary.
- `allowed-explicit`: honor deliberate use of each excluded pattern.
- `non-trigger`, `incidental`, `mechanic`, `canon`: avoid destructive overblocking.
- `paraphrase`, `negative-example`, `partial-permission`: preserve semantic scope.
- `genre-freedom`, `open-generation`: keep useful creativity and the requested format.

## What a pass does not establish

A structural test checks this file's schema/coverage, not the generated answers.
A handful of smoke outputs checks those outputs, not a population-level effect.
Native discovery, automatic triggering, model adherence and reduced default-pattern
frequency are separate questions. For frequency claims, pre-register repetitions,
compare baseline and skill runs with the same prompts/settings, keep independent
sessions, review outputs blind to condition, and report misses and false positives.
Do not omit hard cases after seeing results. No API harness is included because
running this small skill must not require a benchmark platform.

## Observation storage

Use `evals/private/` for raw private runs (gitignored). Commit only sanitized,
consented excerpts. A record should include `case_id`, `skill_sha256`, `cases_sha256`,
`date`, `host`, `observed_model`, `activation`, `output`, `verdict`, `reviewer`, and
`limitations`. New runs never overwrite old outcomes.
