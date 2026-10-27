#!/usr/bin/env python3
"""Create deterministic skill/source ZIPs from a reviewed release allowlist."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import zipfile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check import SKILL_NAME, SKILL_REL, frontmatter, manifest_paths, read_text, validate

# ZIP requires a DOS-encodable timestamp. Fixed for byte-for-byte repeatability.
ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def write_zip(destination: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(root: Path, out: Path) -> dict[str, str]:
    root = root.resolve()
    errors = validate(root)
    if errors:
        raise ValueError("refusing to package invalid repository:\n" + "\n".join(errors))
    version = frontmatter(read_text(root / SKILL_REL / "SKILL.md"))["metadata"]["version"]
    files = manifest_paths(root)
    source_members = {f"{SKILL_NAME}/{p.as_posix()}": (root / p).read_bytes() for p in files}
    skill_files = [p for p in files if p.is_relative_to(SKILL_REL)]
    required = {"SKILL.md", "LICENSE", "references/EVIDENCE.md"}
    actual = {p.relative_to(SKILL_REL).as_posix() for p in skill_files}
    if actual != required:
        raise ValueError("installable skill must contain exactly SKILL.md, LICENSE and evidence")
    skill_members = {f"{SKILL_NAME}/{p.relative_to(SKILL_REL).as_posix()}": (root / p).read_bytes() for p in skill_files}
    out.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    for kind, members in (("skill", skill_members), ("source", source_members)):
        filename = f"{SKILL_NAME}-v{version}-{kind}.zip"
        target = out / filename
        write_zip(target, members)
        hashes[filename] = hashlib.sha256(target.read_bytes()).hexdigest()
    (out / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items())), encoding="utf-8", newline="\n")
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        hashes = build(args.root, args.out or args.root / "dist")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for filename, digest in sorted(hashes.items()):
        print(f"{digest}  {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
