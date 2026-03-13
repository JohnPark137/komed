# Official Downloads Bundle

This directory contains the direct official downloads and locally derived Markdown copies gathered during the ad hoc Korean medicine import run. It is separate from the top-level curated `docs/korean-medicine/` text mirror on purpose.

See also:
- [`MANIFEST.md`](./MANIFEST.md) for a concise inventory.
- [`markdown/README.md`](./markdown/README.md) for the preferred reading copies.

## Layout

- [`pdfs/`](./pdfs/)
  - Original downloaded PDF files.
- [`markdown/`](./markdown/)
  - Markdown converted from those PDFs plus Korean-only companion copies.
- [`archive/`](./archive/)
  - Search notes, raw extraction attempts, and temporary artifacts preserved for traceability.

## PDFs

- [`pdfs/dongui-bogam.pdf`](./pdfs/dongui-bogam.pdf)
- [`pdfs/dongui-bogam-index.pdf`](./pdfs/dongui-bogam-index.pdf)
- [`pdfs/jesebogam.pdf`](./pdfs/jesebogam.pdf)
- [`pdfs/chimgugeukbijeon.pdf`](./pdfs/chimgugeukbijeon.pdf)
- [`pdfs/bangyakhappyeon-vol1.pdf`](./pdfs/bangyakhappyeon-vol1.pdf)

## Markdown

Direct PDF text extraction:
- [`markdown/jesebogam.md`](./markdown/jesebogam.md)
- [`markdown/chimgugeukbijeon.md`](./markdown/chimgugeukbijeon.md)
- [`markdown/bangyakhappyeon-vol1.md`](./markdown/bangyakhappyeon-vol1.md)

Korean-only companion copies:
- [`markdown/dongui-bogam-ko-chapter-index.md`](./markdown/dongui-bogam-ko-chapter-index.md)
- [`markdown/dongui-bogam-ko.md`](./markdown/dongui-bogam-ko.md)
- [`markdown/dongui-bogam-index-ko.md`](./markdown/dongui-bogam-index-ko.md)
- [`markdown/jesebogam-ko.md`](./markdown/jesebogam-ko.md)
- [`markdown/chimgugeukbijeon-ko.md`](./markdown/chimgugeukbijeon-ko.md)
- [`markdown/bangyakhappyeon-vol1-ko.md`](./markdown/bangyakhappyeon-vol1-ko.md)

`dongui-bogam-ko.md` is the canonical full Korean export built from the official `내손안에 동의보감` web reader and covers page `2888`.
`dongui-bogam-ko-chapter-index.md` is the best navigation file for that export.

The lower-quality direct PDF text extracts for full `동의보감` and its index were moved to the archive so the main `markdown/` directory stays focused on the preferred reading copies.

## Provenance Notes

- `dongui-bogam-ko.md` and `dongui-bogam-index-ko.md` were extracted from the official app reader at <https://app.mediclassics.kr>.
- The bookshelf PDFs came from KIOM-hosted official download paths.
- The Markdown files in `markdown/` were generated locally for research convenience and should be treated as derivative working copies, not authoritative editions.

## Archive

- [`archive/search-notes-imported.md`](./archive/search-notes-imported.md)
  - Notes from the official-download discovery run.
- [`archive/dongui-bogam-original.md`](./archive/dongui-bogam-original.md)
  - Earlier raw-text export attempt.
- [`archive/pdf-text-extracts/`](./archive/pdf-text-extracts/)
  - Demoted full-PDF text extraction variants for `동의보감`.
- [`archive/intermediates/`](./archive/intermediates/)
  - Preserved temporary outputs and page fragments from the conversion process.
