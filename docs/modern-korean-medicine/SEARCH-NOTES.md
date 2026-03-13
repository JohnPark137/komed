# Search Notes

Search date: 2026-03-13

## Goal

Find modern `한의학` / Korean medicine textbook-like materials on the public web, verify that they are actually retrievable, and keep local Markdown copies in this repo.

## What Counted As A Good Hit

- Contemporary enough to be useful as modern study/reference material.
- Publicly downloadable from an institutional source.
- Substantial enough to behave like a textbook, handbook, or clinical reference rather than a flyer.
- PDF text extraction had to be usable enough to produce Markdown.

## Selected Sources

1. KIOM English library
   - Main listing: https://kiom.re.kr/gallery.es?mid=a20301010000&bid=0013
   - Best hit: `Introduction to Korean Medicine`
   - Why selected: it is the clearest modern general overview book from an official Korean medicine research institute.

2. NIKOM / National Center for Korean Medicine Clinical Practice Guidelines
   - Portal: https://nikom.or.kr/engnckm/index.do
   - Working PDF pattern: `https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=...`
   - Why selected: these are current, book-length, disease-specific Korean medicine references with explicit institutional provenance and public PDF access.
   - Retrieval note: plain `curl` requests were blocked on some endpoints, so the downloader uses browser-like headers.

## Downloaded In This Run

- `Introduction to Korean Medicine`
- `Clinical Practice Guideline of Korean Medicine for Dizziness`
- `Clinical Practice Guideline of Korean Medicine for Parkinson's Disease`
- `Clinical Practice Guideline of Korean Medicine for Type 2 Diabetes Mellitus`
- `Clinical Practice Guideline of Korean Medicine for Obesity`
- `Clinical Practice Guideline of Korean Medicine for Depression`
- `Clinical Practice Guideline of Korean Medicine for Prostatic Hypertrophy`
- `Clinical Practice Guideline of Korean Medicine for Fracture`

## Searched But Not Added

- KOCW (`kocw.net`)
  - I found Korean medicine course pages, including subjects such as `난경`, `사상의학`, and other lecture entries.
  - These were useful for discovery, but the public assets I found were mainly course pages, video playlists, or syllabi rather than a clean modern textbook corpus.
  - Example search path: `site:kocw.net/home/cview.do 대구한의대학교 한의학`

- Commercial university textbooks and bookstore listings
  - These exist, but mirroring them into the repo would be a straightforward copyright problem.
  - I excluded them entirely.

- Additional KIOM library items
  - The KIOM library page also exposes older or non-textbook items such as multilingual introductions, classical addenda, and illustration sets.
  - I kept only the modern general overview volume for this corpus.

## Practical Conclusion

I did not find a clearly open modern university textbook that could be mirrored wholesale. The strongest legally and technically retrievable substitutes were:

- one official general overview book from KIOM
- multiple up-to-date clinical reference books from NIKOM/NCKM

That is why this folder is framed as a modern Korean medicine reference corpus rather than a single canonical textbook dump.
