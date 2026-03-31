# File Intake Assistant — GUI v0.1 Findings

## Purpose

This file records practical findings from early GUI v0.1 testing.

It is not a changelog and not a final spec.

Its purpose is to capture real behavior, UX problems, and development notes so they are not forgotten during later refinement.

---

## Confirmed positives

### GUI window works
A basic tkinter GUI window can be launched successfully from the current environment.

### Manual path entry works
The GUI path field works and allows direct manual input.

### Preview generation works
The **Preview changes** action successfully runs the existing preview engine and produces:

- `preview.txt`
- `summary.json`
- `records.json`

### Summary line is useful
The summary line is immediately helpful after preview generation and gives a fast overview without opening detailed files.

### Windows path normalization is necessary and useful
Users naturally paste Windows-style paths such as:

`C:\Users\Name\Desktop\Folder Copy`

The GUI should handle this automatically and convert it to WSL format when needed.

---

## Confirmed UX problems

### WSL/Tk folder picker is confusing
The current folder picker does not feel like a normal Windows file picker.

Problems observed:

- navigation is unclear
- it is easy to end up at the wrong location
- it does not feel natural for non-technical users
- it should not be treated as the main civil-friendly folder selection method

### Folder picker behavior feels unreliable
The picker interaction can feel strange, including selection/focus behavior that does not feel normal for a typical Windows user.

### Open preview is not acceptable in current WSL behavior
The current preview opening behavior can launch the preview in a terminal-based editor/viewer.

This is not acceptable for normal users because:

- it is unexpected
- it feels like the user is trapped
- it is unclear how to exit
- it damages trust

### Open preview folder does not work reliably in current WSL environment
Opening the preview folder through the current environment does not behave like a normal Windows folder open action.

This means it is not currently suitable as a reliable civil-friendly fallback in the present setup.

---

## Practical conclusions

### WSL is useful for prototyping GUI structure
The current environment is still useful for:

- layout building
- preview flow testing
- status line testing
- summary line testing
- path handling logic

### WSL is not a reliable reference for final file/folder opening behavior
The current environment should not be treated as the final reference for:

- opening preview files
- opening preview folders
- normal user interaction with file pickers

### Manual path entry is currently the most reliable input method
At this stage, manual path input is more stable and more predictable than relying on the folder picker.

---

## Design implications

### Keep the GUI simple
The current value of the GUI is in:

- selecting or entering a folder
- generating a preview
- showing a summary
- staying clearly preview-only

### Do not rely on terminal-style file opening in a civil-facing version
A normal user should never be pushed into a terminal editor/viewer just to read a preview.

### Final civil-friendly behavior will likely need Windows-side execution
A more realistic civil-facing version will likely require one of the following later:

- Windows Python execution
- packaged Windows build
- a GUI that displays preview content internally

---

## Current recommendation

For the current prototype phase:

- keep testing preview generation
- keep using summary feedback
- keep using manual path entry
- do not trust current WSL preview opening behavior as final UX
- treat current file/folder open behavior as environment-specific findings, not final product behavior

---

## Guiding reminder

The goal is not just to make the GUI run.

The goal is to make it feel safe, obvious, and non-threatening to a normal user.