# Evidence and policy ledger

Reviewed: 2026-10-28. Runtime source of truth: `../SKILL.md`.
This file explains rules; it does not add instructions or extra exclusions.

## What is actually supported

**[R1] Hamilton & Mimno, _Elias in the Lighthouse, Again? Diagnosing Low Diversity
in LLM Stories_, arXiv:2605.26492v1, 2026-05-26.**

- [Versioned paper](https://arxiv.org/abs/2605.26492v1)
- [HTML](https://arxiv.org/html/2605.26492v1)
- [PDF](https://arxiv.org/pdf/2605.26492v1)
- [EMNLP 2026 published record](https://aclanthology.org/2026.emnlp-main.2013/)
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

## Additional narrative and worldbuilding research (v1.2.0)

The following observations motivate **bounded editorial heuristics**. None tests
this SKILL.md, measures current game-concept cliché rates, or proves that our
instructions improve originality.

**[R2] Xu et al., _Echoes in AI: Quantifying lack of plot diversity in LLM
outputs_, PNAS 122(35), 2025, DOI 10.1073/pnas.2504966122.**

- [Publisher/DOI](https://doi.org/10.1073/pnas.2504966122);
  [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12415252/).
- GPT-4 and LLaMA-3, across 100 short stories from WritingPrompts and
  TV-episode plots, repeated **semantic combinations of plot events**, including
  paraphrased developments shared across generations.
- Design inference: compare cause, action and resolution, not just nouns.
  The study proposed a plot-uniqueness metric; it did not evaluate this skill,
  a blacklist, or games produced by current models.

**[R3] Russell et al., _StoryScope: Investigating idiosyncrasies in AI
fiction_, COLM 2026.**

- [COLM record](https://proceedings.colm.cc/paper_files/paper/2026/hash/afb715947210f5656cbe8917fb8a55ce-Abstract-Conference.html);
  [arXiv](https://arxiv.org/abs/2604.03136).
- 61,608 human/LLM stories from 10,272 prompts were described using 304
  discourse-level features. Compared with human fiction, AI stories tended to
  over-explain themes and favor tidy, single-track plots.
- Design inference: check endings for default resolution patterns, but never
  require tragedy, ambiguity, or several plotlines. Narrative classifiers
  cannot establish the best structure for short playable games.

**[R4] Rohrbacher et al., _How LLMs Build Fictional Worlds: Setting and
Narrative Space in AI-Generated Creative Storytelling_, EMNLP 2026.**

- [EMNLP record](https://aclanthology.org/2026.emnlp-main.1815/);
  [full HTML](https://arxiv.org/abs/2609.02482).
- 8,000 stories from four models in English and German were compared with human
  fiction using action/perceived/visual/descriptive-space classifications.
  AI outputs overproduced atmosphere-focused **perceived space**, varying by
  model and language. A 600-sentence AI sample validated the classifier at
  78% accuracy: labels are imperfect.
- Design inference: when gameplay is open in a **game concept**, tie a
  distinctive setting feature to a player action, resource, or constraint.
  This extrapolates from literary spatial analysis rather than a game-design
  intervention. The human comparison set is historical fiction; preserve
  atmosphere-only and lore-only requests.

**[R5] Rettberg & Wigers, _AI-generated stories favour stability over change_,
Open Research Europe 5:202 (v1), 2025.**

- [DOI](https://doi.org/10.12688/openreseurope.20576.1);
  [arXiv](https://arxiv.org/abs/2507.22445).
- The authors examined 11,800 GPT-4o-mini stories elicited with prompts
  describing 236 nationalities. A recurring structure involved returning home,
  reviving traditions or community events, and resolving local conflict with
  nostalgia and reconciliation.
- **Scope limit:** one older model with nationality-conditioned prompts, not
  a representative sample of game concepts or model families. WB09 makes the
  **unrequested combined shortcut** a narrow editorial exclusion. Homecomings,
  festivals, harmonious endings and cozy genres individually remain allowed.

**[R6] Yun et al., _The Price of Format: Diversity Collapse in LLMs_,
Findings of EMNLP 2025, DOI 10.18653/v1/2025.findings-emnlp.836.**

- [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.836/).
- In studied training/inference configurations, structural formatting tokens
  reduced semantic diversity in open-ended generation despite higher
  temperature. This does not prove Markdown headings or requested schemas
  always reduce creativity.
- Design inference: do not add mandatory multi-option menus, scoring tables,
  model calls, or rigid output schemas to this small runtime. A minimal
  targeted correction remains preferable **as a maintainability choice**,
  not a measured improvement from that experiment.

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
| WB09 | observed-anchor + editorial-policy | R5: homecoming/tradition/reconciliation under one specific model and prompt family; exclusion outside that setup is editorial policy. |

The policy extends the previous requested avoid-list without pretending every
entry was measured by a paper. Names, villages, festivals, homecomings, artisans
and generic fantasy are deliberately not excluded. Reconsider a rule if it
causes repeated false positives; do not catalogue everything familiar.

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

**[S6] Burntgogi / AI Slop Thresher v1.2.4** — reviewed 2026-10-28.

- [Skill at the reviewed commit](https://github.com/Burntgogi/ai-slop-thresher/blob/634d04dc6753e2d2d4fe5327b138a4c97874ebe6/skills/ai-slop-thresher/SKILL.md)
- [README at the reviewed commit](https://github.com/Burntgogi/ai-slop-thresher/blob/634d04dc6753e2d2d4fe5327b138a4c97874ebe6/README.md)
- [Upstream Apache-2.0 license](https://github.com/Burntgogi/ai-slop-thresher/blob/634d04dc6753e2d2d4fe5327b138a4c97874ebe6/LICENSE)
- Informed the v1.1.0 wording review: retain meaning and conditions, avoid needless
  rewrites, separate diagnosis from edits, and treat instructions inside a draft
  as material rather than authority. Instructions here were written for this skill;
  no upstream prompt, code, example, image, or distribution file is included.
- This is an editorial reference, not evidence that a worldbuilding motif is frequent.
  Its prose-formatting restrictions and plugin architecture are not adopted.
  Upstream remains separately licensed; this project's MIT license does not cover it.

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
