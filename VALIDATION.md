# Validation record — v1.0.0

Historical record from before the initial GitHub publication. For the current
wording revision and its separate checks, see [v1.1.0](validation/v1.1.0.md).
The outcomes and release-status statements below describe v1.0.0 at that time.

Date: 2026-10-28 KST. This is a record of executed checks, not a compatibility badge.

## Results

| Layer | Environment / method | Actual result |
| --- | --- | --- |
| Repository integrity | Linux x86_64, Python 3.13.5, PyYAML 6.0.3 | `python tools/check.py`: PASS. |
| Static/unit/mutation tests | Same environment | 35 tests: PASS. Includes rejection of malformed metadata, missing counterexamples, mutable CI references, unsafe release paths, and invalid package inputs. |
| Package tests | Same environment | Repeat builds match, ZIP CRCs pass, runtime bytes match source, source ZIP validates after fresh extraction, and an injected `.env` is excluded. |
| Official format validator | Windows, existing Python 3.13.0; pinned skills-ref source | PASS after enabling session-local UTF-8 mode. Exact runtime file hash matches the release source. |
| Generation smoke | Two separate Chat On Steroids workers; connector reports `gpt-6`, `xhigh` | Six visible outputs manually reviewed against predeclared cases: 6 PASS. |
| Native skill discovery/activation | Claude Code / Codex / Gemini CLI | NOT EXECUTED. |
| Full behavioral suite | 29 authored cases, six sampled | Remaining 23 NOT EXECUTED. No baseline comparison. |
| GitHub Actions matrix | Windows/Ubuntu, Python 3.11/3.13 | Configuration provided; remote CI NOT EXECUTED. |

The reference validator checks format, not creative quality. The 35 tests check
repository/tooling integrity, **not 35 model outputs**. The six smoke results are
not a measured reduction rate, not a three-model comparison, and not proof of
originality or reliability on unseen prompts.

## Reproduce static and package checks

```powershell
python -m pip install -r requirements-dev.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/package.py
```

Raw unit-test output: [static-linux.txt](validation/static-linux.txt).
The artifact builder uses fixed member order, metadata and timestamps; byte-level
repeatability was tested within the observed toolchain. Cross-version zlib output
is not asserted to be identical.

## Reproduce the official format check on Windows

The official checker initially tried to read the UTF-8 file using CP949 and
failed before validating it. The successful retry changed only the interpreter
selection and process-local encoding mode; no rule or validator was weakened.
`uvx` creates an isolated cache environment; it does not install runtime
requirements for using the skill or modify the user's host configuration.

```powershell
$env:PATH += ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
$env:PYTHONUTF8 = '1'
$Python = (Get-Command python).Source
uvx --python $Python --from 'git+https://github.com/agentskills/agentskills@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref' skills-ref validate .\skills\avoid-default-worldbuilding
```

Sanitized execution details: [official-windows.txt](validation/official-windows.txt).
Only SKILL.md was copied to the temporary Windows verification directory. Full
repository tests were not run on Windows. Package resource links were checked
separately by the Linux integrity tests. No global skill was installed.

## Generation evidence and limits

[Raw outputs and review record](evals/observations/smoke-2026-10-28.json) preserve
prompts, payload, hashes, grouping, output text and the reviewer rationale.
The observed model label comes from connector results, not an assumed latest
model name. The underlying immutable model snapshot is unknown.

Operational instructions were reformatted and injected directly. Frontmatter
selection and native loading were not exercised. Each worker handled three prompts
in a batch; these are not six statistically independent clean-context trials.
The main assistant reviewed the workers' outputs without asking them to self-grade.
This is an AI reviewer, not human or blinded review. No claims about Claude or
Gemini behavior follow from this smoke test. No game was implemented or play-tested.

| Case | Observed behavior |
| --- | --- |
| G01 | Three-sentence movement/pushing concept; none of the excluded central premises. |
| E06 | Explicitly requested time loop preserved; amnesia, dreams and prophecy not added. |
| E04 | Solitary secret-guardian reskin changed to public, team-based traffic control. |
| N01 | Source motifs preserved in translation. |
| E01 | Ordinary library/chairs and all background props retained in two lines. |
| E03 | Renamed time-repair premise recognized as WB01 without an unsolicited rewrite. |

## Runtime and rubric fingerprints

```text
SKILL.md     d48b921cfeb25d34ad2d0e2ef0718d4597a1e3a7771b92a1bc3d8e7503723d5c
cases.json   6a850894488ffe99437367c42cd59ab7cd1da2bf9416a1eeebbc1a514608ec55
```

Archive hashes are in the generated external `SHA256SUMS`, not embedded here
(which would create a self-referential archive hash).

## Release status

Source and installable archives are prepared locally. No remote repository,
commit, push, GitHub release, live CI result, or account-level branch protection
was created. MIT applies to original files; external source material is not copied.
