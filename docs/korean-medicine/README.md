# Open Korean Medicine Texts

Search date: 2026-03-12

This directory is organized into two distinct collections:

- Top-level `dongui-bogam-*.md` files: curated, openly reusable text gathered from Wikisource plus Korean companion files aligned to the official `내손안에 동의보감` translation layer.
- [`official-downloads/`](./official-downloads/): locally stored PDFs and Markdown derived from direct official downloads gathered in a later ad hoc run.

## Directory Layout

- [`INDEX.md`](./INDEX.md)
  - Single-page entry point for the whole corpus.
- Top-level Markdown files
  - Reusable `동의보감` source text and Korean companion text that fit the original curation goal of this folder.
- [`MANIFEST.md`](./MANIFEST.md)
  - Inventory for the curated top-level text set.
- [`SEARCH-NOTES.md`](./SEARCH-NOTES.md)
  - Broader search log for the curated text run.
- [`official-downloads/`](./official-downloads/)
  - Official PDF downloads, locally derived Markdown copies, and archived one-off extraction artifacts.
  - See [`official-downloads/MANIFEST.md`](./official-downloads/MANIFEST.md) for the imported bundle inventory.

## Curated Text Set

The top-level files remain centered on `동의보감` because that is where the best combination of open reuse, public availability, and machine-readable structure exists.

Original-heavy files from Korean Wikisource:
- [dongui-bogam-seomun.md](./dongui-bogam-seomun.md)
- [dongui-bogam-jibrye.md](./dongui-bogam-jibrye.md)
- [dongui-bogam-naegyeongpyeon.md](./dongui-bogam-naegyeongpyeon.md)
- [dongui-bogam-oehyeongpyeon.md](./dongui-bogam-oehyeongpyeon.md)
- [dongui-bogam-japbyeongpyeon.md](./dongui-bogam-japbyeongpyeon.md)
- [dongui-bogam-chimgupyeon.md](./dongui-bogam-chimgupyeon.md)

Official Korean companion files:
- [dongui-bogam-seomun-ko.md](./dongui-bogam-seomun-ko.md)
- [dongui-bogam-jibrye-ko.md](./dongui-bogam-jibrye-ko.md)
- [dongui-bogam-naegyeongpyeon-ko.md](./dongui-bogam-naegyeongpyeon-ko.md)
- [dongui-bogam-oehyeongpyeon-ko.md](./dongui-bogam-oehyeongpyeon-ko.md)
- [dongui-bogam-japbyeongpyeon-ko.md](./dongui-bogam-japbyeongpyeon-ko.md)
- [dongui-bogam-chimgupyeon-ko.md](./dongui-bogam-chimgupyeon-ko.md)

These `-ko.md` files were extracted from the `KO` blocks already present in the official app pages. They were not machine-translated.

## Official Downloads Bundle

The later download/conversion run produced a separate local reference bundle under [`official-downloads/`](./official-downloads/). That bundle includes:

- Original PDFs under [`official-downloads/pdfs/`](./official-downloads/pdfs/)
- Markdown converted from those PDFs under [`official-downloads/markdown/`](./official-downloads/markdown/)
- Archived one-off notes and failed extraction artifacts under [`official-downloads/archive/`](./official-downloads/archive/)

Read [`official-downloads/README.md`](./official-downloads/README.md) before reusing those files. They were kept for local research convenience, not as part of the stricter reusable-text mirror described above.

## Sources

- Korean Wikisource `동의보감`
  - <https://ko.wikisource.org/wiki/동의보감>
- KIOM raw-text distribution for `동의보감`
  - <https://info.mediclassics.kr/apps/dist-texts/index.html#/Book/8>
- Official `내손안에 동의보감` app
  - <https://app.mediclassics.kr/books/동의보감>

## Reproduction

- Download reusable text set: `python3 scripts/download_korean_medicine_texts.py`
- Build official Korean companions for the curated set: `python3 scripts/build_korean_companions.py`
- Convert downloaded PDFs to Markdown: `python3 scripts/pdf_to_markdown.py`

## Caveats

- Historical/traditional content should not be treated as current medical guidance.
- The Wikisource files are cleaned from wiki markup, not hand-edited scholarly editions.
- The official-downloads bundle has different provenance and licensing constraints than the curated top-level mirror.
