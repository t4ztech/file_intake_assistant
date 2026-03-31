# File Intake Assistant — Minimal GUI v0.1 Spec

## Goal

Create the simplest possible GUI layer for File Intake Assistant so non-technical users can generate and open a safe preview without using the terminal.

This version is preview-only.

It must not rename, move, or apply changes.

---

## Core idea

Preview file cleanup before changing anything.

---

## Safety principle

WARNING: MAKE A COPY OF YOUR ORIGINAL FOLDER FIRST

This version creates a preview only.

Hidden files and hidden folders should be skipped by default for safety.

---

## GUI purpose

The GUI is a thin layer on top of the existing preview engine.

It should let the user:

- choose a folder copy
- generate a preview
- open the detailed preview
- open the preview results folder

---

## Main user flow

1. Open the GUI
2. See the warning
3. Click **Choose folder**
4. Select a copied folder
5. Click **Preview changes**
6. Review the summary
7. Click **Open preview**
8. If needed, click **Open preview folder**

---

## Window text

### Title
File Intake Assistant

### Subtitle
Preview file cleanup before changing anything.

### Warning
WARNING: MAKE A COPY OF YOUR ORIGINAL FOLDER FIRST  
This version creates a preview only.

---

## Main controls

### 1. Choose folder
Select the folder copy you want to preview.

### 2. Preview changes
Create a preview plan without changing any files.

### 3. Open preview
Open `preview.txt` in your default text editor.

### 4. Open preview folder
Open the folder that contains the preview results.

---

## Selected folder line

### Before selection
Selected folder: none

### After selection
Selected folder: C:\Users\Name\Desktop\Test_Copy

---

## Status messages

- Status: No folder selected
- Status: Folder selected
- Status: Preview created successfully
- Status: Could not create preview
- Status: Preview file not found
- Status: Could not open preview automatically

---

## Summary line

### Before preview
No preview yet

### After preview
Scanned: 30 | Documents: 20 | Images: 9 | Other: 1 | Renames: 25 | Moves: 30

---

## Required behavior

### Choose folder
- opens the normal folder picker
- stores the selected folder path
- updates the selected folder line
- resets the summary line to `No preview yet`

### Preview changes
- requires a selected folder
- runs preview only
- creates:
  - `preview.txt`
  - `summary.json`
  - `records.json`
- updates the status line
- updates the summary line

### Open preview
- opens `preview.txt`
- does not create a new preview
- if `preview.txt` is missing, update status

### Open preview folder
- opens the preview results folder
- acts as a fallback if preview cannot be opened automatically

---

## Out of scope for v0.1

Do not include:

- Apply changes
- Recursive scan options in GUI
- Date prefix options in GUI
- Drag and drop
- Settings panel
- History
- Advanced filters
- Built-in text viewer
- EXE packaging
- Full desktop app behavior

---

## Design direction

The GUI must feel:

- simple
- safe
- clear
- non-technical
- predictable

The tool should not feel “smart”.
It should feel safe and understandable.

---

## Product philosophy

Check first. Change later.