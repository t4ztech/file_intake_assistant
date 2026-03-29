
# File Intake Assistant

A simple CLI tool for inspecting, previewing, renaming, and organizing messy folders safely.

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