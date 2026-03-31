# Changelog

## v1.3

This update focused on making preview results safer and more practical on real mixed desktop-style folders.

### Improvements
- skipped `.lnk` files by default
- skipped `.url` files by default
- classified `.odt` files as `documents`
- classified `.html` files as `documents`

### Why this mattered
Earlier preview results were too aggressive on real desktop-copy test folders. Shortcuts, URLs, and document-like files were being grouped too broadly into `other`, which made the preview less trustworthy.

### Result
The preview became more focused and safer:

- fewer unnecessary rename/move suggestions
- much smaller `other` category
- more realistic document classification
- better fit for safety-first cleanup review