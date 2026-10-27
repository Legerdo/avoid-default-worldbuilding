---
name: avoid-default-worldbuilding
description: Avoid stock AI worldbuilding when inventing or revising game concepts, story premises, settings, or lore (세계관, 컨셉, 클리셰 회피). Use for unspecified creative choices or an explicit anti-cliche review. Preserve requested themes and established canon. Do not rewrite facts, translations, summaries, or code-only tasks.
license: MIT
metadata:
  version: "1.0.0"
---

# Avoid Default Worldbuilding

Choose a coherent premise without falling back on the patterns below. This is
an editorial avoid-list, not a ranking of every model's most frequent outputs.
It needs no scripts, API calls, external searches, or extra user questionnaires.

## Boundaries

- Apply only to creative choices the user has left open. Explicit requirements
  and established project canon take priority; change canon only when requested.
- A genre, mood, or visual style does not authorize every trope associated with it.
  Conversely, preserve a requested mechanic even when its name resembles a trope.
- An example to avoid, a quotation, or an unapproved draft is not user approval.
- Do not alter translations, summaries, factual descriptions, or implementation-only
  work. For a critique, diagnose rather than rewrite unless rewriting was requested.

## Default exclusions

Exclude these from an **unrequested central premise**: the protagonist's defining
role, the world's causal rule, the main conflict, or its resolution. Match meaning
across languages, renamed jobs, and genre reskins, not isolated keywords.

| ID | Central pattern to avoid by default |
| --- | --- |
| WB01 | Clock/watchmaker lead; a world repaired through clocks, stopped time, time loops, or rewinding history. |
| WB02 | A lonely lighthouse/beacon keeper protecting an old secret; the same setup moved to a tower or space station. |
| WB03 | Amnesia or collecting, trading, restoring, or erasing memories as the route to the protagonist's identity or the world's truth. |
| WB04 | A librarian/archivist lead or a magical library, forbidden book, or archive that contains or rewrites the world's hidden truth. |
| WB05 | Collecting or repairing dreams, a dream world, or a collapsing dream/reality boundary as the premise or final explanation. |
| WB06 | An extinct civilization's relics, scattered sacred fragments, or a sealed ancient power that must restore the world's lost balance. |
| WB07 | Prophecy, a chosen bloodline, or predestined exceptional status that makes the hero the world's designated savior. |
| WB08 | Portals, dimensional rifts, or doors between worlds used as an unexplained origin, central mystery, or catch-all resolution. |

## Apply without overblocking

1. Keep the user's constraints, requested genre/mechanics, and established canon.
   Permission for one pattern is narrow: it does not authorize the other patterns.
2. Check the proposed premise once against WB01-WB08. If it matches without that
   permission, replace its causal setup, role, conflict, or solution. Renaming a
   clockmaker as a "chronal engineer" is not a replacement.
3. Build the replacement around a concrete activity, constraint, relationship,
   or stake. Keep it understandable and feasible. Do not add arbitrary weirdness
   or repeatedly substitute one new favorite occupation or genre.
4. Keep incidental objects and ordinary functions: a background clock, a coastal
   landmark, a diary, a school library, a ruin, or a normal recollection is allowed.
   A countdown, undo control, retry, respawn, or fast-travel mechanic alone is not
   world lore. Do not invent prohibited lore to explain it.
5. Recheck the final premise, including its twist and ending. Do not add an excluded
   explanation late in implementation. Do not expand the user's requested output.

Do not ban all fantasy, mystery, magic, villages, artisans, or familiar names.
Do not reject the task or demand a new concept when the user deliberately requests
an excluded pattern. Use it, keeping any other explicit exclusions intact.

## Output

Return the requested artifact, in the user's language and format. Keep this
checklist and discarded candidates out of the default answer. On a requested
review, give the matched rule and a brief, concrete reason; offer a rewrite only
when requested. Do not claim that passing this check proves originality.

Maintenance provenance: [EVIDENCE.md](references/EVIDENCE.md). Reading it is
optional during creative work; all operational rules are above.
