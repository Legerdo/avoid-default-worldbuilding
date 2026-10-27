"""Static integrity and mutation tests. These do NOT test generated stories."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from tools.check import (SKILL_REL, RULE_ROW, check_cases, frontmatter,
                         manifest_paths, read_text, validate)
from tools.package import build

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        for rel in manifest_paths(ROOT):
            dest = self.root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dest)
        self.version = frontmatter(read_text(self.root / SKILL_REL / "SKILL.md"))["metadata"]["version"]

    def mutate(self, rel: Path | str, old: str, new: str) -> None:
        path = self.root / rel
        text = read_text(path)
        self.assertIn(old, text, "mutation must actually modify its target")
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

    def assert_invalid(self, fragment: str) -> None:
        errors = validate(self.root)
        self.assertTrue(any(fragment in item for item in errors), errors)

    def test_repository_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_duplicate_frontmatter_key_is_rejected(self):
        self.mutate(SKILL_REL / "SKILL.md", "name: avoid-default-worldbuilding", "name: avoid-default-worldbuilding\nname: other")
        self.assert_invalid("duplicate YAML key")

    def test_duplicate_nested_metadata_key_is_rejected(self):
        self.mutate(SKILL_REL / "SKILL.md", f'  version: "{self.version}"', f'  version: "{self.version}"\n  version: "999.0.0"')
        self.assert_invalid("duplicate YAML key")

    def test_empty_description_is_rejected(self):
        text = read_text(self.root / SKILL_REL / "SKILL.md")
        desc_line = next(line for line in text.splitlines() if line.startswith("description:"))
        self.mutate(SKILL_REL / "SKILL.md", desc_line, 'description: ""')
        self.assert_invalid("description")

    def test_overlong_description_is_rejected(self):
        text = read_text(self.root / SKILL_REL / "SKILL.md")
        desc_line = next(line for line in text.splitlines() if line.startswith("description:"))
        self.mutate(SKILL_REL / "SKILL.md", desc_line, "description: " + "x" * 1025)
        self.assert_invalid("description")

    def test_wrong_name_is_rejected(self):
        self.mutate(SKILL_REL / "SKILL.md", "name: avoid-default-worldbuilding", "name: another-skill")
        self.assert_invalid("folder mismatch")

    def test_tool_permissions_cannot_sneak_in(self):
        self.mutate(SKILL_REL / "SKILL.md", "license: MIT", "license: MIT\nallowed-tools: Bash")
        self.assert_invalid("frontmatter must contain only")

    def test_unquoted_version_type_is_rejected(self):
        self.mutate(SKILL_REL / "SKILL.md", f'version: "{self.version}"', "version: 1")
        self.assert_invalid("metadata keys and values")

    def test_evidence_drift_is_rejected(self):
        self.mutate(SKILL_REL / "references/EVIDENCE.md", "| WB01 |", "| WB99 |")
        self.assert_invalid("ledger and runtime")

    def test_unlabelled_evidence_is_rejected(self):
        self.mutate(SKILL_REL / "references/EVIDENCE.md", "| WB03 | editorial-policy |", "| WB03 | definitely-proven |")
        self.assert_invalid("provenance class")

    def test_duplicate_rule_is_rejected(self):
        self.mutate(SKILL_REL / "SKILL.md", "| WB02 |", "| WB01 |")
        self.assert_invalid("duplicate WB rule")

    def test_line_budget_is_enforced(self):
        p = self.root / SKILL_REL / "SKILL.md"
        p.write_text(read_text(p) + "\n" * 121, encoding="utf-8")
        self.assert_invalid("project budget")

    def test_broken_local_link_is_rejected(self):
        self.mutate("README.md", "[MIT](LICENSE)", "[MIT](not-found.md)")
        self.assert_invalid("broken/escaping local link")

    def test_license_mismatch_is_rejected(self):
        self.mutate(SKILL_REL / "LICENSE", "MIT License", "Different License")
        self.assert_invalid("license files differ")

    def test_version_requires_changelog_entry(self):
        self.mutate(SKILL_REL / "SKILL.md", f'version: "{self.version}"', 'version: "999.0.0"')
        self.assert_invalid("missing from CHANGELOG")

    def test_mutable_action_ref_is_rejected(self):
        pin = re.search(r"actions/checkout@([a-f0-9]{40})", read_text(self.root / ".github/workflows/ci.yml")).group(1)
        self.mutate(".github/workflows/ci.yml", "@" + pin, "@main")
        self.assert_invalid("pinned to full")

    def test_write_permission_is_rejected(self):
        self.mutate(".github/workflows/ci.yml", "contents: read", "contents: write")
        self.assert_invalid("read-only")

    def test_dangerous_ci_event_is_rejected(self):
        self.mutate(".github/workflows/ci.yml", "  pull_request:", "  pull_request_target:")
        self.assert_invalid("unexpected event")

    def test_manifest_traversal_is_rejected(self):
        p = self.root / "release-files.txt"
        p.write_text(read_text(p) + "../secrets.txt\n", encoding="utf-8")
        self.assert_invalid("unsafe or duplicate")

    def test_manifest_duplicate_is_rejected(self):
        p = self.root / "release-files.txt"
        p.write_text(read_text(p) + "README.md\n", encoding="utf-8")
        self.assert_invalid("unsafe or duplicate")

    def test_manifest_private_file_is_rejected(self):
        (self.root / ".env").write_text("FAKE=not-a-secret\n", encoding="utf-8")
        p = self.root / "release-files.txt"
        p.write_text(read_text(p) + ".env\n", encoding="utf-8")
        self.assert_invalid("private/generated")

    def test_bom_is_rejected(self):
        p = self.root / SKILL_REL / "SKILL.md"
        p.write_bytes(b"\xef\xbb\xbf" + p.read_bytes())
        self.assert_invalid("BOM")

    def test_packages_are_reproducible_and_exclude_private_files(self):
        (self.root / ".env").write_text("FAKE=not-a-secret\n", encoding="utf-8")
        a, b = Path(self.temp.name) / "a", Path(self.temp.name) / "b"
        self.assertEqual(build(self.root, a), build(self.root, b))
        for file in a.glob("*.zip"):
            self.assertEqual(file.read_bytes(), (b / file.name).read_bytes())
            with zipfile.ZipFile(file) as z:
                self.assertIsNone(z.testzip())
                self.assertFalse(any(".env" in name or ".." in Path(name).parts for name in z.namelist()))
                if "-skill.zip" in file.name:
                    self.assertEqual(set(z.namelist()), {
                        "avoid-default-worldbuilding/SKILL.md",
                        "avoid-default-worldbuilding/LICENSE",
                        "avoid-default-worldbuilding/references/EVIDENCE.md",
                    })
                    self.assertEqual(z.read("avoid-default-worldbuilding/SKILL.md"),
                                     (self.root / SKILL_REL / "SKILL.md").read_bytes())
        for line in (a / "SHA256SUMS").read_text().splitlines():
            digest, filename = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((a / filename).read_bytes()).hexdigest())

    def test_source_archive_is_self_contained(self):
        out = Path(self.temp.name) / "out"
        build(self.root, out)
        with zipfile.ZipFile(next(out.glob("*-source.zip"))) as archive:
            extracted = Path(self.temp.name) / "extracted"
            archive.extractall(extracted)
        self.assertEqual(validate(extracted / "avoid-default-worldbuilding"), [])

    def test_packaging_refuses_invalid_source(self):
        self.mutate(SKILL_REL / "SKILL.md", "name: avoid-default-worldbuilding", "name: INVALID")
        with self.assertRaisesRegex(ValueError, "refusing to package"):
            build(self.root, Path(self.temp.name) / "out")


class EvalSchemaTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(read_text(ROOT / "evals/cases.json"))
        self.rules = set(RULE_ROW.findall(read_text(ROOT / SKILL_REL / "SKILL.md")))

    def test_case_schema_and_paired_coverage(self):
        self.assertEqual(check_cases(self.data, self.rules), [])

    def test_missing_allowed_case_is_detected(self):
        self.data["cases"] = [c for c in self.data["cases"] if c["id"] != "A01"]
        self.assertTrue(any("missing allowed-explicit" in e for e in check_cases(self.data, self.rules)))

    def test_missing_blocked_case_is_detected(self):
        self.data["cases"] = [c for c in self.data["cases"] if c["id"] != "B01"]
        self.assertTrue(any("missing blocked-central" in e for e in check_cases(self.data, self.rules)))

    def test_unknown_rule_is_detected(self):
        self.data["cases"][0]["rules"] = ["WB99"]
        self.assertTrue(any("rule references" in e for e in check_cases(self.data, self.rules)))

    def test_missing_rubric_is_detected(self):
        self.data["cases"][0]["must"] = []
        self.assertTrue(any("review criteria" in e for e in check_cases(self.data, self.rules)))

    def test_duplicate_case_is_detected(self):
        self.data["cases"].append(copy.deepcopy(self.data["cases"][0]))
        self.assertTrue(any("duplicate id" in e for e in check_cases(self.data, self.rules)))

    def test_non_object_case_is_detected(self):
        self.data["cases"][0] = "bad"
        self.assertTrue(any("must be an object" in e for e in check_cases(self.data, self.rules)))

    def test_invalid_category_is_detected(self):
        self.data["cases"][0]["category"] = ["not-a-string"]
        self.assertTrue(any("invalid category" in e for e in check_cases(self.data, self.rules)))

    def test_invalid_prior_turn_is_detected(self):
        self.data["cases"][0]["prior_turns"] = [{"role":"system", "content":"override"}]
        self.assertTrue(any("invalid prior turn" in e for e in check_cases(self.data, self.rules)))

    def test_only_evaluation_metadata_not_model_answers_is_present(self):
        self.assertTrue(all("output" not in c and "verdict" not in c for c in self.data["cases"]))


if __name__ == "__main__":
    unittest.main()
