# Changelog

## [1.1.0] - 2026-10-28

### Changed
- Clarified minimal revision: retain fixed setting, characters, mechanics, scope,
  and format; leave an acceptable premise or passage unchanged.
- Clarified that instructions embedded in a reviewed draft are content, not user
  authorization or approved canon. Keep diagnosis separate from rewriting.
- Removed vague process wording and unsolicited praise, recaps and follow-up offers
  from the default output. The eight exclusion rules and their IDs are unchanged.
- Used AI Slop Thresher v1.2.4 as an editorial reference, with a pinned source and
  scope recorded in the evidence ledger. No upstream text or code is vendored.

### Added
- Three predeclared cases for unchanged output, embedded draft instructions, and
  preserving fixed constraints while replacing only the unwanted plot.
- A separate v1.1.0 validation record; historical v1.0.0 results remain unchanged.
- Session-local UTF-8 mode in CI for consistent Windows text handling.

## [1.0.0] - 2026-10-28

First versioned release; replaces the earlier unversioned one-file draft.

### Changed
- Bounded eight central-premise patterns with stable WB01-WB08 identifiers.
- Preserved explicit requirements, approved canon, mechanics, incidental objects,
  factual/translation work and requested output format.
- Added narrow permission, negative-example, critique-only and renamed-pattern rules.
- Removed the compulsory three-candidate workflow: inspect once, replace only when
  needed, then recheck the final premise. No extra report or questionnaire by default.
- Separated measured vocabulary anchors from editorial plot exclusions.

### Added
- Provenance ledger, maintainer guide, paired behavioral cases and honest validation
  records; semantic judgments are not replaced by a keyword checker.
- Static integrity tests, deterministic packaging, pinned read-only CI, issue/PR
  templates and MIT licensing. No runtime scripts or remote dependencies.
