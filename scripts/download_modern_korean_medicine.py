#!/usr/bin/env python3
"""Download a modern Korean medicine reference corpus and convert it to Markdown."""

from __future__ import annotations

import subprocess
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "modern-korean-medicine"
PDF_DIR = OUTPUT_DIR / "pdfs"
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
DOWNLOAD_DATE = "2026-03-13"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
}

NIKOM_HEADERS = {
    **DEFAULT_HEADERS,
    "Referer": "https://nikom.or.kr/engnckm/index.do",
}

SOURCES = [
    {
        "slug": "introduction-to-korean-medicine",
        "title": "Introduction to Korean Medicine",
        "organization": "Korean Institute of Oriental Medicine (KIOM)",
        "kind": "overview book",
        "language": "English",
        "year": "2014 (PDF metadata)",
        "source_page": "https://kiom.re.kr/gallery.es?mid=a20301010000&bid=0013&act=view&list_no=1542",
        "pdf_url": "https://kiom.re.kr/galleryDownload.es?bid=0013&list_no=1542&seq=2",
        "headers": DEFAULT_HEADERS,
        "note": "Public KIOM library download. The landing page describes five overview chapters, and the PDF cover reads `Introduction to Traditional Korean Medicine`.",
    },
    {
        "slug": "km-cpg-dizziness",
        "title": "Clinical Practice Guideline of Korean Medicine for Dizziness",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean",
        "year": "2021",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=145",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=145",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. Extracted title text identifies the topic as `현훈`.",
    },
    {
        "slug": "km-cpg-parkinsons-disease",
        "title": "Clinical Practice Guideline of Korean Medicine for Parkinson's Disease",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean",
        "year": "2021",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=214",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=214",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. Extracted text identifies the topic as `파킨슨병`.",
    },
    {
        "slug": "km-cpg-type-2-diabetes-mellitus",
        "title": "Clinical Practice Guideline of Korean Medicine for Type 2 Diabetes Mellitus",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean with English subtitle",
        "year": "2023",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=295",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=295",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. Extracted text explicitly includes `Type 2 Diabetes Mellitus` and `2형 당뇨병`.",
    },
    {
        "slug": "km-cpg-obesity",
        "title": "Clinical Practice Guideline of Korean Medicine for Obesity",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean with English subtitle",
        "year": "2024",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=328",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=328",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. The title page is bilingual and marks the topic as obesity.",
    },
    {
        "slug": "km-cpg-depression",
        "title": "Clinical Practice Guideline of Korean Medicine for Depression",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean",
        "year": "2024",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=337",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=337",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. Extracted text identifies the topic as `우울증` and states that the guideline reflects updated research.",
    },
    {
        "slug": "km-cpg-prostatic-hypertrophy",
        "title": "Clinical Practice Guideline of Korean Medicine for Prostatic Hypertrophy",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean with English subtitle",
        "year": "2024",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=351",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=351",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. The title page is bilingual and covers `전립선증식증`.",
    },
    {
        "slug": "km-cpg-fracture",
        "title": "Clinical Practice Guideline of Korean Medicine for Fracture",
        "organization": "National Institute for Korean Medicine Development (NIKOM)",
        "kind": "clinical practice guideline",
        "language": "Korean with English subtitle",
        "year": "2025",
        "source_page": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=653",
        "pdf_url": "https://nikom.or.kr/engnckm/module/practiceGuide/viewPDF.do?guide_idx=653",
        "headers": NIKOM_HEADERS,
        "note": "Public PDF from the NCKM portal. The title page is bilingual and the PDF metadata dates it to 2025.",
    },
]


def ensure_dirs() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)


def run_curl(url: str, output_path: Path, headers: dict[str, str]) -> None:
    command = [
        "curl",
        "--http1.1",
        "-L",
        "-s",
        "--fail",
        "--connect-timeout",
        "20",
        "--max-time",
        "300",
        "--retry",
        "3",
        "--retry-all-errors",
        url,
        "-o",
        str(output_path),
    ]
    for key, value in headers.items():
        command.extend(["-H", f"{key}: {value}"])
    subprocess.run(command, check=True)


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = text.replace("\t", " ")
    text = text.replace("\r", "\n")
    lines = [" ".join(line.split()) for line in text.splitlines()]

    cleaned: list[str] = []
    blank_run = 0
    for line in lines:
        if not line:
            blank_run += 1
            if blank_run <= 1:
                cleaned.append("")
            continue
        blank_run = 0
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def convert_pdf(source: dict, pdf_path: Path) -> tuple[Path, int]:
    reader = PdfReader(str(pdf_path))
    md_path = MARKDOWN_DIR / f"{source['slug']}.md"
    parts = [
        f"# {source['title']}",
        "",
        f"- Organization: {source['organization']}",
        f"- Type: {source['kind']}",
        f"- Language: {source['language']}",
        f"- Year: {source['year']}",
        f"- Source page: {source['source_page']}",
        f"- Source PDF: {source['pdf_url']}",
        f"- Downloaded: {DOWNLOAD_DATE}",
        f"- Local PDF: `pdfs/{pdf_path.name}`",
        "",
        "---",
        "",
    ]

    for index, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text() or "")
        if not text:
            continue
        parts.append(f"## Page {index}")
        parts.append("")
        parts.append(text)
        parts.append("")

    md_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return md_path, len(reader.pages)


def format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def write_readme(records: list[dict]) -> None:
    lines = [
        "# Modern Korean Medicine References",
        "",
        f"Search and download date: {DOWNLOAD_DATE}",
        "",
        "This folder contains modern, public, textbook-like Korean medicine references converted into Markdown for local research use. I did not find a clearly open-license, contemporary university textbook that could be mirrored wholesale, so this corpus focuses on the strongest official alternatives: a general KIOM overview book and current NIKOM/NCKM clinical practice guideline books.",
        "",
        "## What Was Included",
        "",
        "- Official public PDFs from KIOM and NIKOM/NCKM.",
        "- Materials substantial enough to function as study references rather than one-page brochures.",
        "- Files that converted to machine-readable text well enough to be usable as Markdown.",
        "",
        "## Rights Caveat",
        "",
        "These Markdown files are local text extractions from publicly downloadable PDFs. The source institutions retain their copyrights and terms. This folder is for local research/workspace use, not a claim that the converted Markdown is newly relicensed.",
        "",
        "## Files",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"- [`markdown/{record['md_path'].name}`](./markdown/{record['md_path'].name})",
                f"  - Title: {record['title']}",
                f"  - Source organization: {record['organization']}",
                f"  - Type: {record['kind']}",
                f"  - Language: {record['language']}",
                f"  - Pages: {record['pages']}",
                f"  - Markdown size: {format_size(record['md_path'].stat().st_size)}",
                f"  - PDF: [`pdfs/{record['pdf_path'].name}`](./pdfs/{record['pdf_path'].name})",
                f"  - PDF size: {format_size(record['pdf_path'].stat().st_size)}",
            ]
        )
    lines.extend(
        [
            "",
            "## Reproduction",
            "",
            "- Run: `python3 scripts/download_modern_korean_medicine.py`",
            f"- Output: `{OUTPUT_DIR.relative_to(ROOT)}/`",
            "",
            "## Search Notes",
            "",
            "- See [`SEARCH-NOTES.md`](./SEARCH-NOTES.md) for the wider search, rejected source classes, and why this set was selected.",
            "- See [`MANIFEST.md`](./MANIFEST.md) for the full inventory and source URLs.",
            "",
        ]
    )
    (OUTPUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(records: list[dict]) -> None:
    lines = [
        "# Manifest",
        "",
        f"Generated: {DOWNLOAD_DATE}",
        "",
        "| Markdown | Title | Pages | Language | PDF Size | Source |",
        "| --- | --- | ---: | --- | ---: | --- |",
    ]
    for record in records:
        lines.append(
            "| "
            f"[`markdown/{record['md_path'].name}`](./markdown/{record['md_path'].name}) | "
            f"{record['title']} | "
            f"{record['pages']} | "
            f"{record['language']} | "
            f"{format_size(record['pdf_path'].stat().st_size)} | "
            f"{record['source_page']} |"
        )
    lines.append("")
    (OUTPUT_DIR / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")


def write_search_notes() -> None:
    content = f"""# Search Notes

Search date: {DOWNLOAD_DATE}

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
"""
    (OUTPUT_DIR / "SEARCH-NOTES.md").write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    records: list[dict] = []

    for source in SOURCES:
        pdf_path = PDF_DIR / f"{source['slug']}.pdf"
        print(f"Downloading {source['title']}", flush=True)
        run_curl(source["pdf_url"], pdf_path, source["headers"])
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise RuntimeError(f"Download failed for {source['title']}")
        md_path, pages = convert_pdf(source, pdf_path)
        records.append(
            {
                **source,
                "pdf_path": pdf_path,
                "md_path": md_path,
                "pages": pages,
            }
        )

    write_readme(records)
    write_manifest(records)
    write_search_notes()
    print(f"Wrote {len(records)} Markdown files to {MARKDOWN_DIR}", flush=True)


if __name__ == "__main__":
    main()
