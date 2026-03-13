# Intermediate Artifacts

This directory keeps temporary files from the import and conversion workflow that were moved out of the main bundle during cleanup.

## Contents

- `dongui-bogam-ko-sequential.md`
  - Earlier sequential build of the full Korean `동의보감` export.
- `dongui-bogam-ko-page-fragments/`
  - Per-page fragments used to assemble the parallel full export.
- `api-chunks/`
  - Partial JSON responses from the raw KIOM API fetch attempt.
- `extraction-work/`
  - Scratch TSV files from Markdown conversion experiments.

These files are not the preferred entry points for reading. Use the canonical files under:
- [`../../markdown/`](../../markdown/)
- [`../../pdfs/`](../../pdfs/)
