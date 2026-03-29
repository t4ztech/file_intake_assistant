
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