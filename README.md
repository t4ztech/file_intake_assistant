START README
# File Intake Assistant

A simple CLI tool for inspecting, previewing, renaming, and organizing messy folders safely.

## Who this is for

File Intake Assistant is designed for solo operators and small teams who deal with messy folders full of mixed files such as photos, PDFs, scans, exports, and documents.

## Why this tool exists

Manual file cleanup is slow, repetitive, and easy to mess up. This tool helps inspect a folder first, preview safe renaming and category-based organization, and only apply changes after confirmation.

## Safety-first workflow

The tool is designed around a simple rule:

- inspect first
- preview changes
- confirm before apply

## What it does

- scans a folder
- counts files by category
- flags suspicious file names
- detects duplicate file names
- previews cleaned file names
- previews category-based folder organization
- can apply rename + move operations
- writes summary and operation reports

## Current categories

- images
- documents
- archives
- audio
- video
- other

## Safe workflow

### Preview only

Run the tool without `--apply` first.

Example:

```bash
python3 file_intake_assistant_v1.py --root test_input --output-dir output_test
```

This generates:

- `summary.json`
- `records.json`
- `preview.txt`

### Apply changes

Only use `--apply` after checking the preview.

Example:

```bash
python3 file_intake_assistant_v1.py --root test_input --output-dir output_test --apply
```

## Optional flags

### Recursive scan

```bash
python3 file_intake_assistant_v1.py --root test_input --output-dir output_test --recursive
```

In recursive mode, the tool scans files in subfolders and can still preview rename suggestions, but category-based move actions are disabled for safety.

### Add date prefix to cleaned names

```bash
python3 file_intake_assistant_v1.py --root test_input --output-dir output_test --date-prefix
```

## Current limitations

- no undo yet
- no hash-based duplicate detection yet
- no GUI
- no cloud or Google Drive integration
- no content analysis inside files

## Status

Current version: MVP v1.2  
Working features tested in WSL Ubuntu terminal.

## Tested scenarios

- preview scan on messy flat folder
- apply mode on messy flat folder
- rerun preview on already organized folder
- filename collision handling with safe suffix numbering
- empty folder handling
- no-changes-needed messaging
- recursive real-world preview with move actions disabled for safety

## Known limitations

- duplicate detection is currently based on file names, not file content hashes
- no undo support yet
- no custom naming templates yet
- category organization is currently fixed by extension mapping
END README