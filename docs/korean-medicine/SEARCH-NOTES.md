# Search Notes

Search date: 2026-03-12

## Goal

Find Korean medicine texts that are both publicly reachable and legally safe enough to copy into this repository as Markdown.

## Sources Checked

### Korean Wikisource

- Main entry checked: <https://ko.wikisource.org/wiki/동의보감>
- Outcome: usable
- Reason: text pages are publicly accessible in raw wiki form and can be converted into plain Markdown with lightweight cleanup.
- Files taken from this source:
  - `동의보감/서문`
  - `동의보감/집례`
  - `동의보감/내경편`
  - `동의보감/외형편`
  - `동의보감/잡병편`
  - `동의보감/침구편`

### KIOM Raw-Text Distribution

- Source page: <https://info.mediclassics.kr/apps/dist-texts/index.html#/Book/8>
- Outcome: source approved, full fresh mirror not completed in this run
- Reason: the page explicitly allows non-commercial use with attribution to `한의학고전DB(mediclassics.kr)`, but the volume content API was too slow and unstable for a complete 23-volume pull during this session.

### Official App Translation Layer

- Source page: <https://app.mediclassics.kr/books/동의보감>
- Outcome: used for Korean companion copies
- Reason: the official app page HTML exposes aligned `OR`, `KO`, and `EN` blocks for page content, which makes it possible to extract the site's own Korean translation rather than attempting model-generated translation.
- Resulting files:
  - `dongui-bogam-seomun-ko.md`
  - `dongui-bogam-jibrye-ko.md`
  - `dongui-bogam-naegyeongpyeon-ko.md`
  - `dongui-bogam-oehyeongpyeon-ko.md`
  - `dongui-bogam-japbyeongpyeon-ko.md`
  - `dongui-bogam-chimgupyeon-ko.md`

### KIOM Bookshelf eBooks

- Source list: <https://info.mediclassics.kr/bookshelf/list/eBook/list>
- Terms page: <https://info.mediclassics.kr/bookshelf/terms_of_service>
- Outcome: not copied
- Reason: the terms state `CC BY-NC-ND 4.0` and also state that the content should not be reposted online or transformed into derivative works. Markdown conversion for local repo redistribution would be too risky under those terms.

### English Wikibooks

- Query used: <https://en.wikibooks.org/w/api.php?action=query&list=search&srsearch=%22Korean%20medicine%22%20OR%20%22Han%20medicine%22%20OR%20%22Dongui%20Bogam%22&format=json>
- Outcome: no relevant book pages

### Korean Wikibooks

- Query used: <https://ko.wikibooks.org/w/api.php?action=query&list=search&srsearch=동의보감%20OR%20한의학%20OR%20한국%20의학&format=json>
- Outcome: no comparable Korean medicine classic suitable for download

### Internet Archive

- Outcome: searched, not selected
- Reason: the results were weaker than KIOM and Wikisource for clear provenance plus reusable full text.

## Selection Logic

- Prefer sources with explicit reuse language over sources that are merely public to read.
- Prefer machine-readable text over scan-only PDFs.
- Reject sources with no-derivatives restrictions for repo redistribution.
- Keep provenance in every Markdown file header.

## Known Gaps

- This folder currently emphasizes `동의보감` because it is the most practical open source currently identified in this search.
- A future pass could keep working on the KIOM raw API with more aggressive retry, checkpointing, or a cached chunk downloader.
- The official app delivers content by page, so the Korean companion files are organized by page number rather than by a fully reflowed scholarly chapter structure.
