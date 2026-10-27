# Evidence and policy ledger

Reviewed: 2026-10-28. Runtime source of truth: `../SKILL.md`.
This file explains rules; it does not add instructions or extra exclusions.

## What is actually supported

**[R1] Hamilton & Mimno, _Elias in the Lighthouse, Again? Diagnosing Low Diversity
in LLM Stories_, arXiv:2605.26492v1, 2026-05-26.**

- [Versioned paper](https://arxiv.org/abs/2605.26492v1)
- [HTML](https://arxiv.org/html/2605.26492v1)
- [PDF](https://arxiv.org/pdf/2605.26492v1)
- Reviewed: Section 3; Appendix B / Table 4; Appendix C / Table 5.
  PDF pages 2 and 7 were visually inspected.
- The experiment generated 20,000 English stories using five short prompts and
  four models: Claude Haiku 4.5, GPT-5.4-Mini, Gemini 3.1 Flash-Lite, OLMo 7b Thinking.
  Recurrent vocabulary includes lighthouse, keeper, clockmaker, librarian and names.
  Archivist appears in the additional vocabulary rather than the core set.
- Limits: lexical occurrence is not a measurement of whole plot combinations.
  This is not a Korean game-concept benchmark or evidence about every later model.
  In Table 5, clockmaker is not especially prevalent in the tested Claude model.
  The skill therefore has no vendor-specific stereotype or model-frequency ranking.
- Original data, prose, figures and implementation are not copied into this package.

## Rule-by-rule scope

`observed-anchor` means only the named ingredient has evidence in R1.
`editorial-policy` means a deliberate creative preference, not an empirical claim.
All eight rules have the same override behavior in SKILL.md.

| Rule | Evidence class | Supported anchor / boundary of claim |
| --- | --- | --- |
| WB01 | observed-anchor + editorial-policy | R1: clockmaker; time manipulation and loop extensions are policy. |
| WB02 | observed-anchor + editorial-policy | R1: lighthouse / keeper; reskins and the general secret-guardian structure are policy. |
| WB03 | editorial-policy | Memory-based identity or world-revelation plots are a chosen exclusion; no prevalence claim. |
| WB04 | observed-anchor + editorial-policy | R1: librarian, plus archivist in Appendix B; magical books rewriting truth are policy. |
| WB05 | editorial-policy | Dream-based worlds or explanations are a chosen exclusion; no prevalence claim. |
| WB06 | editorial-policy | Relic restoration / lost-balance plots are a chosen exclusion, not a ban on all ruins. |
| WB07 | editorial-policy | Predestined-savior plots are a chosen exclusion, not a ban on heroes or fantasy. |
| WB08 | editorial-policy | Unexplained dimensional plot devices are a chosen exclusion, not a ban on travel mechanics. |

The policy extends the previous requested avoid-list without pretending every
entry was measured by a paper. Names, all villages, all artisans and generic
fantasy are deliberately not excluded. Reconsider a rule if it causes repeated
false positives; do not turn the list into a catalogue of everything familiar.

## Format and implementation references

**[S1] Agent Skills specification** — [official specification](https://agentskills.io/specification).
Reviewed naming, frontmatter, optional resources and progressive disclosure.
The runtime follows the common format rather than vendor-only frontmatter.

**[S2] Anthropic skill-creator** — [official source](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md).
Reviewed iterative test-and-review workflow. No code or prompts were vendored.
Our static checks and manually judged behavioral samples remain distinct.

**[S3] Claude Code** — [skills documentation](https://code.claude.com/docs/en/skills).
Source for `.claude/skills` installation and explicit slash invocation.

**[S4] OpenAI Codex** — [skills documentation](https://developers.openai.com/codex/skills/).
Source for `.agents/skills` discovery. The URL redirected to OpenAI's
[Build skills guide](https://learn.chatgpt.com/docs/build-skills) during review.

**[S5] Gemini CLI** — [skills documentation](https://geminicli.com/docs/cli/skills/).
Source for `.gemini/skills`, the `.agents/skills` alias and `/skills list`.
These sources describe host support, not proof that this particular skill loads
or improves generation in every host.

## Reuse decision

The [AIStoryHub corpus](https://github.com/AIStoryHub/AIStoryHub_LLM_Cliche_Corpus)
was reviewed as a related project. It is not a dependency. Its lists, code and
license claims are not imported. This skill needs a small, bounded premise policy,
not a large prose/style corpus. Unverified prior claims about repository counts,
licenses, recent model names or benchmark scores are not inherited here.

## Change discipline

Record a dated primary source and exact scope before calling an ingredient
empirically observed. A hypothesis or user's repeated observation can justify an
editorial policy but must remain labelled as such. Keep the original scope and
record corrections in CHANGELOG.md rather than silently rewriting the evidence.
