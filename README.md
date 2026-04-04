# File Intake Assistant

A safety-first CLI tool for cleaning up mixed-file folders without blindly renaming and moving everything.

Preview file cleanup before changing anything.

Check first. Change later.

## Why this tool exists

Manual file cleanup is slow, repetitive, and easy to mess up. File Intake Assistant helps you inspect a folder first, preview safe renaming and category-based organization, and only apply changes after confirmation.

## Who this is for

File Intake Assistant is designed for solo operators and small teams who deal with messy folders full of mixed files such as photos, PDFs, scans, exports, and documents.

## Safety-first workflow

The tool is built around a simple rule:

- inspect first
- preview changes
- confirm before apply

## WARNING !!!

**1. MAKE A COPY OF YOUR ORIGINAL FOLDER**

Do not test File Intake Assistant on your original folder first.

Make a copy of the folder, run preview mode on that copy, and review the suggested changes before using `--apply`.

## What it does

- scans a folder
- counts files by category
- flags suspicious file names
- detects duplicate file names
- previews cleaned file names
- previews category-based folder organization
- can apply rename + move operations
- writes summary and operation reports

## Recent improvement

Version 1.3 focused on safety improvements based on real mixed-folder testing.

- skipped `.lnk` files by default
- skipped `.url` files by default
- classified `.odt` files as documents
- classified `.html` files as documents

This made preview results less aggressive and reduced unnecessary cleanup suggestions on real desktop-style folder tests.

## Current categories

- images
- documents
- archives
- audio
- video
- other

## Example before and after

### Before

- `IMG 001.JPG`
- `scan(1).pdf`
- `final  final report.txt`
- `weird@name!.csv`

### After

- `images/img_001.jpg`
- `documents/scan_1.pdf`
- `documents/final_final_report.txt`
- `documents/weird_name.csv`

## Safe workflow

### Preview only

Run the tool without `--apply` first.

Example:

```bash
python3 file_intake_assistant_v1.py --root test_input --output-dir output_test