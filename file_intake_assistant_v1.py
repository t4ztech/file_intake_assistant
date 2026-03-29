from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

SAFE_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}
SAFE_DOC_EXTS = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md", ".xls", ".xlsx", ".csv"}
SAFE_ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz"}
SAFE_AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".flac", ".aac"}
SAFE_VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".wmv"}

CATEGORY_MAP = {
    "images": SAFE_IMAGE_EXTS,
    "documents": SAFE_DOC_EXTS,
    "archives": SAFE_ARCHIVE_EXTS,
    "audio": SAFE_AUDIO_EXTS,
    "video": SAFE_VIDEO_EXTS,
}

INVALID_NAME_RE = re.compile(r"[^A-Za-z0-9._ -]+")
MULTISPACE_RE = re.compile(r"\s+")


@dataclass
class FileRecord:
    path: str
    name: str
    extension: str
    size_bytes: int
    modified_iso: str
    category: str
    suspicious_name: bool
    duplicate_name_count: int = 1
    planned_name: str | None = None
    planned_category_folder: str | None = None


@dataclass
class Summary:
    root_folder: str
    scanned_files: int
    files_by_category: dict[str, int]
    suspicious_names: int
    duplicate_names: int
    planned_renames: int
    planned_moves: int
    generated_at: str


def iter_files(root: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        yield from (p for p in root.rglob("*") if p.is_file())
    else:
        yield from (p for p in root.iterdir() if p.is_file())


def categorize_file(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "other"


def is_suspicious_name(name: str) -> bool:
    if INVALID_NAME_RE.search(name):
        return True
    if "  " in name:
        return True
    if name != name.strip():
        return True
    return False


def clean_stem(stem: str) -> str:
    stem = stem.strip()
    stem = INVALID_NAME_RE.sub("_", stem)
    stem = MULTISPACE_RE.sub(" ", stem)
    stem = stem.replace(" ", "_")
    stem = re.sub(r"_+", "_", stem)
    stem = stem.strip("._-")
    return stem.lower() or "unnamed"


def build_records(root: Path, recursive: bool) -> list[FileRecord]:
    files = sorted(iter_files(root, recursive), key=lambda p: str(p).lower())
    name_counts = Counter(f.name.lower() for f in files)
    records: list[FileRecord] = []

    for file_path in files:
        stat = file_path.stat()
        record = FileRecord(
            path=str(file_path),
            name=file_path.name,
            extension=file_path.suffix.lower(),
            size_bytes=stat.st_size,
            modified_iso=datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            category=categorize_file(file_path.suffix),
            suspicious_name=is_suspicious_name(file_path.name),
            duplicate_name_count=name_counts[file_path.name.lower()],
        )
        records.append(record)

    return records


def plan_renames(records: list[FileRecord], date_prefix: bool) -> None:
    seen_names: Counter[str] = Counter()

    for record in records:
        original = Path(record.name)
        cleaned_stem = clean_stem(original.stem)
        parts = []
        if date_prefix:
            parts.append(record.modified_iso[:10])
        parts.append(cleaned_stem)
        new_stem = "_".join(p for p in parts if p)
        candidate = f"{new_stem}{record.extension}"

        seen_names[candidate] += 1
        if seen_names[candidate] > 1:
            candidate = f"{new_stem}_{seen_names[candidate]:03d}{record.extension}"

        if candidate != record.name:
            record.planned_name = candidate

def plan_organization(records: list[FileRecord], root: Path) -> None:
    for record in records:
        record_path = Path(record.path)
        relative_parent = record_path.parent.relative_to(root)

        if relative_parent == Path(record.category):
            record.planned_category_folder = None
        else:
            record.planned_category_folder = record.category


def make_summary(root: Path, records: list[FileRecord]) -> Summary:
    files_by_category = Counter(r.category for r in records)
    suspicious_names = sum(1 for r in records if r.suspicious_name)
    duplicate_names = sum(1 for r in records if r.duplicate_name_count > 1)
    planned_renames = sum(1 for r in records if r.planned_name)
    planned_moves = sum(1 for r in records if r.planned_category_folder)

    return Summary(
        root_folder=str(root),
        scanned_files=len(records),
        files_by_category=dict(sorted(files_by_category.items())),
        suspicious_names=suspicious_names,
        duplicate_names=duplicate_names,
        planned_renames=planned_renames,
        planned_moves=planned_moves,
        generated_at=datetime.now().isoformat(timespec="seconds"),
    )


def write_report(output_dir: Path, summary: Summary, records: list[FileRecord]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "summary.json"
    records_path = output_dir / "records.json"
    preview_path = output_dir / "preview.txt"

    summary_path.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
    records_path.write_text(json.dumps([asdict(r) for r in records], indent=2), encoding="utf-8")

    lines = []
    lines.append("FILE INTAKE ASSISTANT PREVIEW")
    lines.append(f"Generated: {summary.generated_at}")
    lines.append(f"Root: {summary.root_folder}")
    lines.append("")
    lines.append(f"Scanned files: {summary.scanned_files}")
    lines.append(f"Suspicious names: {summary.suspicious_names}")
    lines.append(f"Duplicate names: {summary.duplicate_names}")
    lines.append(f"Planned renames: {summary.planned_renames}")
    lines.append(f"Planned moves: {summary.planned_moves}")
    lines.append("")
    lines.append("Files by category:")
    for category, count in summary.files_by_category.items():
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("Planned actions:")
    for record in records:
        if record.planned_name or record.planned_category_folder:
            action_bits = [record.name]
            if record.planned_name:
                action_bits.append(f"rename -> {record.planned_name}")
            if record.planned_category_folder:
                action_bits.append(f"move -> {record.planned_category_folder}/")
            lines.append(" | ".join(action_bits))

    preview_path.write_text("\n".join(lines), encoding="utf-8")


def apply_changes(root: Path, records: list[FileRecord], output_dir: Path) -> None:
    operations_log = []

    for record in records:
        source = Path(record.path)
        target_dir = root / (record.planned_category_folder or "")
        target_dir.mkdir(parents=True, exist_ok=True)
        target_name = record.planned_name or source.name
        target = target_dir / target_name

        if source.resolve() == target.resolve():
            continue

        if target.exists():
            operations_log.append({
                "status": "skipped_exists",
                "source": str(source),
                "target": str(target),
            })
            continue

        shutil.move(str(source), str(target))
        operations_log.append({
            "status": "moved",
            "source": str(source),
            "target": str(target),
        })

    (output_dir / "operations_log.json").write_text(
        json.dumps(operations_log, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect, preview, rename, and organize messy folders safely."
    )
    parser.add_argument("--root", required=True, help="Root folder to inspect")
    parser.add_argument(
        "--output-dir",
        default="fia_output",
        help="Folder for summary and preview reports",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include files in subfolders",
    )
    parser.add_argument(
        "--date-prefix",
        action="store_true",
        help="Prefix cleaned file names with modified date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename and move files. Without this flag, preview only.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root folder does not exist or is not a directory: {root}")

    records = build_records(root, recursive=args.recursive)
    plan_renames(records, date_prefix=args.date_prefix)
    plan_organization(records, root)
    summary = make_summary(root, records)
    write_report(output_dir, summary, records)

    if args.apply:
        apply_changes(root, records, output_dir)
        print(f"Applied changes. See reports in: {output_dir}")
    else:
        print(f"Preview only. See reports in: {output_dir}")


if __name__ == "__main__":
    main()
