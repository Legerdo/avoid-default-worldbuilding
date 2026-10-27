#!/usr/bin/env python3
"""Check repository integrity, never semantic quality of model-generated text."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

import yaml

SKILL_NAME = "avoid-default-worldbuilding"
SKILL_REL = Path("skills") / SKILL_NAME
# Project size budget, not an Agent Skills specification limit.
MAINTENANCE_LINE_BUDGET = 120
FRONTMATTER_FIELDS = {"name", "description", "license", "metadata"}
CASE_CATEGORIES = {
    "blocked-central", "allowed-explicit", "non-trigger", "incidental", "mechanic",
    "paraphrase", "negative-example", "partial-permission", "canon", "genre-freedom",
    "open-generation",
}
CASE_REQUIRED = {"id", "category", "rules", "prompt", "must", "must_not"}
CASE_OPTIONAL = {"candidate_fixture", "prior_turns"}
RULE_ROW = re.compile(r"^\| (WB\d{2}) \|", re.MULTILINE)
SEMVER = re.compile(r"\d+\.\d+\.\d+")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject silent YAML key overrides in metadata and workflow configuration."""


def _mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise ValueError("YAML keys must be scalar")
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def read_text(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not permitted: {path.name}")
    text = data.decode("utf-8")
    if "\x00" in text:
        raise ValueError(f"NUL in text: {path.name}")
    return text


def frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    obj = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    if not isinstance(obj, dict):
        raise ValueError("frontmatter must be a mapping")
    return obj


def manifest_paths(root: Path) -> list[Path]:
    """A reviewed release allowlist; reject traversal, duplicates and symlinks."""
    root = root.resolve()
    entries: list[Path] = []
    seen: set[str] = set()
    for raw in read_text(root / "release-files.txt").splitlines():
        item = raw.strip()
        if not item or item.startswith("#"):
            continue
        rel = PurePosixPath(item)
        if (rel.is_absolute() or ".." in rel.parts or "\\" in item or ":" in item
                or item != rel.as_posix() or item in seen):
            raise ValueError(f"unsafe or duplicate release path: {item}")
        seen.add(item)
        candidate = root / Path(*rel.parts)
        if any(parent.is_symlink() for parent in [candidate, *candidate.parents]
               if parent != root and parent.is_relative_to(root)):
            raise ValueError(f"symlink is not allowed in release: {item}")
        if not candidate.resolve().is_relative_to(root) or not candidate.is_file():
            raise ValueError(f"missing or escaping release path: {item}")
        if any(part in {".git", ".venv", "__pycache__", "private", "dist"}
               or part.startswith(".env") for part in rel.parts):
            raise ValueError(f"private/generated release path: {item}")
        if candidate.suffix not in {".md", ".py", ".json", ".yml", ".txt", ""} and item not in {".gitignore", ".gitattributes"}:
            raise ValueError(f"unsupported release file type: {item}")
        entries.append(Path(*rel.parts))
    if not entries:
        raise ValueError("empty release manifest")
    return entries


def check_cases(data: Any, rule_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or set(data) != {"schema_version", "cases"}:
        return ["eval file must contain only schema_version and cases"]
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        errors.append("unsupported eval schema_version")
    cases = data["cases"]
    if not isinstance(cases, list) or not cases:
        return errors + ["eval cases must be a non-empty list"]
    seen: set[str] = set()
    categories: set[str] = set()
    coverage = {"blocked-central": set(), "allowed-explicit": set()}
    for i, case in enumerate(cases):
        label = f"eval[{i}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: case must be an object")
            continue
        if not CASE_REQUIRED.issubset(case) or set(case) - CASE_REQUIRED - CASE_OPTIONAL:
            errors.append(f"{label}: unexpected or missing fields")
            continue
        cid = case["id"]
        if not isinstance(cid, str) or not re.fullmatch(r"[A-Z]\d{2}", cid) or cid in seen:
            errors.append(f"{label}: invalid/duplicate id")
        else:
            seen.add(cid)
        cat = case["category"]
        valid_cat = isinstance(cat, str) and cat in CASE_CATEGORIES
        if not valid_cat:
            errors.append(f"{label}: invalid category")
        else:
            categories.add(cat)
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            errors.append(f"{label}: prompt must be a non-empty string")
        rules = case["rules"]
        valid_rules = isinstance(rules, list) and all(isinstance(r, str) and r in rule_ids for r in rules)
        if not valid_rules or (valid_rules and len(rules) != len(set(rules))):
            errors.append(f"{label}: invalid/duplicate rule references")
        elif valid_cat and cat in coverage:
            if not rules:
                errors.append(f"{label}: paired case requires a rule")
            coverage[cat].update(rules)
        for field in ("must", "must_not"):
            items = case[field]
            if not isinstance(items, list) or not items or not all(isinstance(v, str) and v.strip() for v in items):
                errors.append(f"{label}: {field} must contain non-empty review criteria")
        if valid_cat and cat == "blocked-central":
            if not isinstance(case.get("candidate_fixture"), str) or not case["candidate_fixture"].strip():
                errors.append(f"{label}: blocked case requires an authored candidate_fixture")
        if "prior_turns" in case:
            turns = case["prior_turns"]
            if not isinstance(turns, list) or not turns:
                errors.append(f"{label}: invalid prior_turns")
            else:
                for turn in turns:
                    if (not isinstance(turn, dict) or set(turn) != {"role", "content"}
                            or turn["role"] not in ("user", "assistant")
                            or not isinstance(turn["content"], str) or not turn["content"].strip()):
                        errors.append(f"{label}: invalid prior turn")
    for cat, covered in coverage.items():
        if rule_ids - covered:
            errors.append(f"missing {cat} cases: {sorted(rule_ids - covered)}")
    if CASE_CATEGORIES - categories:
        errors.append(f"missing regression categories: {sorted(CASE_CATEGORIES - categories)}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    try:
        files = manifest_paths(root)
        skill_path = root / SKILL_REL / "SKILL.md"
        text = read_text(skill_path)
        meta = frontmatter(text)
        if set(meta) != FRONTMATTER_FIELDS:
            errors.append("runtime frontmatter must contain only name, description, license and metadata")
        name = meta.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != skill_path.parent.name:
            errors.append("invalid skill name or folder mismatch")
        desc = meta.get("description")
        if not isinstance(desc, str) or not 1 <= len(desc.strip()) <= 1024:
            errors.append("description must be 1..1024 characters")
        if meta.get("license") != "MIT":
            errors.append("license must match the packaged MIT license")
        metadata = meta.get("metadata")
        if not isinstance(metadata, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()):
            errors.append("metadata keys and values must be strings")
            version = ""
        else:
            version = metadata.get("version", "")
            if not SEMVER.fullmatch(version):
                errors.append("metadata.version must be x.y.z")
        if len(text.splitlines()) > MAINTENANCE_LINE_BUDGET:
            errors.append(f"SKILL.md exceeds project budget of {MAINTENANCE_LINE_BUDGET} lines")
        ids = RULE_ROW.findall(text)
        if not ids or len(ids) != len(set(ids)):
            errors.append("missing or duplicate WB rule rows")
        evidence = read_text(root / SKILL_REL / "references/EVIDENCE.md")
        evidence_ids = RULE_ROW.findall(evidence)
        if set(ids) != set(evidence_ids) or len(evidence_ids) != len(set(evidence_ids)):
            errors.append("evidence ledger and runtime rule IDs differ")
        for line in evidence.splitlines():
            if RULE_ROW.match(line) and not any(label in line for label in ("observed-anchor", "editorial-policy")):
                errors.append("evidence rule lacks a provenance class")
        cases = json.loads(read_text(root / "evals/cases.json"))
        errors.extend(check_cases(cases, set(ids)))
        if version and f"## [{version}]" not in read_text(root / "CHANGELOG.md"):
            errors.append("current version is missing from CHANGELOG.md")
        if read_text(root / "LICENSE") != read_text(root / SKILL_REL / "LICENSE"):
            errors.append("root and installable license files differ")
        ci_text = read_text(root / ".github/workflows/ci.yml")
        # BaseLoader avoids YAML 1.1 interpreting GitHub's 'on' as a Boolean.
        ci = yaml.load(ci_text, Loader=yaml.BaseLoader)
        if ci.get("permissions") != {"contents": "read"}:
            errors.append("CI must have read-only contents permission")
        if set(ci.get("on", {})) != {"push", "pull_request", "workflow_dispatch"}:
            errors.append("CI has unexpected event triggers")
        for step in ci["jobs"]["validate"]["steps"]:
            if "uses" in step and not re.fullmatch(r"[\w.-]+/[\w.-]+@[a-f0-9]{40}", step["uses"]):
                errors.append("CI actions must be pinned to full commit SHAs")
        for rel in files:
            source = read_text(root / rel)
            if not source.endswith("\n"):
                errors.append(f"missing final newline: {rel.as_posix()}")
            if rel.suffix != ".md":
                continue
            for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", source):
                if re.match(r"[a-zA-Z][\w+.-]*:", link) or link.startswith("#"):
                    continue
                target = (root / rel.parent / link.split("#", 1)[0]).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    errors.append(f"broken/escaping local link: {rel.as_posix()} -> {link}")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        errors.append(f"integrity check could not complete: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: repository structure, provenance IDs, case coverage, links and release inputs.")
    print("NOT TESTED by this command: model behavior, host activation or cliché reduction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
