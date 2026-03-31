# File Intake Assistant — Roadmap

## Current state

File Intake Assistant currently works as a safety-first CLI tool for previewing folder cleanup before applying changes.

The current foundation includes:

- folder inspection
- preview-first workflow
- rename suggestions
- category-based organization preview
- summary and preview report generation
- safety warning in README
- changelog tracking
- v1.3 safety improvements based on real mixed-folder testing

## Completed recently

### v1.3 safety pass
Recent improvements focused on making preview results safer and more practical on real desktop-style folder copies.

Completed improvements:

- skipped `.lnk` files by default
- skipped `.url` files by default
- classified `.odt` files as `documents`
- classified `.html` files as `documents`

This reduced unnecessary suggestions and made preview results more trustworthy.

## Next step

### Minimal GUI v0.1
The next practical goal is to build a minimal GUI layer on top of the existing preview engine.

The purpose of this GUI is simple:

- remove terminal friction
- make first use easier
- keep the tool safety-first
- let non-technical users generate a preview without needing command-line knowledge

The GUI should remain preview-only.

It should not apply changes in v0.1.

## GUI v0.1 goals

The first GUI version should allow the user to:

- choose a folder copy
- generate a preview
- open `preview.txt`
- open the preview folder
- see a short status message
- see a short preview summary

## GUI v0.1 principles

- preview first
- no automatic file changes
- strong safety warning
- simple language
- clear fallback behavior
- hidden files and hidden folders skipped by default for safety

## After GUI v0.1

After the first GUI prototype is built, the next step is real testing on copied folders.

That testing should focus on:

- clarity of wording
- ease of use
- whether the buttons feel obvious
- whether the preview summary is useful
- where normal users get confused
- where the workflow still feels too technical

## Later direction

Possible later steps may include:

- easier first-run experience
- packaging for simpler Windows use
- broader testing with non-technical users
- improved rename rules
- improved category handling
- more refined preview behavior based on real feedback

## Guiding idea

Check first. Change later.