# Contributing

## Scope

Maintain a small worldbuilding avoidance skill, not a prose humanizer, plagiarism
detector, creativity benchmark, trope encyclopedia, or model-ranking service.
Runtime policy lives only in SKILL.md. Do not add a second runtime JSON catalogue,
a dependency, model API call, or mandatory research step to creative execution.

## Change protocol

1. Reproduce the unwanted **central premise**, recording the prompt, unedited
   output, host, model identifier when observable, date and skill version.
   Redact private information before committing; never include credentials.
2. Check whether an existing WB rule already covers it. Clarify that rule before
   adding a new one. New policy must be narrower than an entire genre.
3. Add a unique stable WB ID only when needed. Never renumber or reuse an old ID.
   Label evidence as `observed-anchor` and/or `editorial-policy` in EVIDENCE.md.
   A repeated personal observation is useful but is not a frequency estimate.
4. Add a failing example and at least one closely related allowed boundary case
   to `evals/cases.json`. Add explicit-request and paraphrase cases when relevant.
   Update acceptance criteria **before** collecting new outputs. Review policy
   changes separately from changes to the tests or grading criteria.
5. Modify SKILL.md, bump `metadata.version`, and describe the behavioral change
   in CHANGELOG.md. The package version comes from SKILL.md, not another constant.
6. Run `python tools/check.py`, `python -m unittest discover -s tests -v`, and
   `python tools/package.py`. Review the exact ZIP member list and hashes.
7. Run affected behavioral cases in fresh sessions; keep raw outputs and document
   reviewer identity/method. For releases claiming reduced cliché frequency, run
   paired baseline/skill generations under the same recorded settings. Without
   that experiment, report only the smoke cases actually exercised.

## Version policy

- PATCH: spelling, documentation or tooling fixes without intended policy change.
- MINOR: a new exclusion, new trigger or narrower/wider behavior within the scope.
- MAJOR: incompatible behavior, such as changing explicit-request/canon precedence.

Removing a rule can change outputs; do not disguise it as a documentation patch.
Keep retired IDs in the changelog. Preserve old evaluation runs as historical
records; do not rewrite their recorded results after changing the skill.

## Review gates

A semantic reviewer checks: scope/consent, central versus incidental meaning,
renamed equivalents, playability/coherence, and unwanted changes to output format.
Keyword counts and an agent's own PASS declaration are not semantic verification.
Do not make the writer its own sole grader. Do not silently change expected
results to make a failed run pass. Record disagreements rather than forcing green.

GitHub CI performs static integrity and packaging tests, not live model calls.
Branch protection and required reviews must be enabled by the repository owner;
these files do not enforce account-level permissions on their own.

## Dependencies and sources

There are no runtime dependencies. PyYAML is development-only. GitHub Actions
are pinned to verified full commit hashes. Review updates rather than replacing
pins with mutable branches. Official validation can be run with the pinned
reference implementation documented in VALIDATION.md; it is not vendored.
Use primary sources, preserve version/scope, and do not copy research datasets,
large quotations, or third-party skill text into this repository.
