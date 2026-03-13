#!/usr/bin/env python3
"""Download and document openly reusable Korean medicine text sources."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "korean-medicine"
DOWNLOAD_DATE = "2026-03-12"

KIOM_API_ROOT = "https://mediclassics.kr/api/books/8/volumes"
KIOM_HEADERS = {
    "Authorization": "5fe23edf9dec4c718e188073e46274bd",
    "Content-Type": "application/json",
    "User-Agent": "codex-downloader/1.0",
}

WIKISOURCE_PAGES = [
    ("dongui-bogam-seomun.md", "동의보감/서문"),
    ("dongui-bogam-jibrye.md", "동의보감/집례"),
    ("dongui-bogam-naegyeongpyeon.md", "동의보감/내경편"),
    ("dongui-bogam-oehyeongpyeon.md", "동의보감/외형편"),
    ("dongui-bogam-japbyeongpyeon.md", "동의보감/잡병편"),
    ("dongui-bogam-chimgupyeon.md", "동의보감/침구편"),
]


PAGE_DESCRIPTIONS = {
    "dongui-bogam-seomun.md": "Preface text from Korean Wikisource.",
    "dongui-bogam-jibrye.md": "Editorial and organizational notes (`집례`).",
    "dongui-bogam-naegyeongpyeon.md": "Internal landscape section (`내경편`).",
    "dongui-bogam-oehyeongpyeon.md": "External form section (`외형편`).",
    "dongui-bogam-japbyeongpyeon.md": "General diseases section (`잡병편`).",
    "dongui-bogam-chimgupyeon.md": "Acupuncture and moxibustion section (`침구편`).",
    "kiom-dongui-bogam-original.md": "Optional official KIOM raw-text export when `--include-kiom` is used.",
}


def fetch_text(url: str, headers: dict[str, str] | None = None) -> str:
    command = [
        "curl",
        "--http1.1",
        "-L",
        "-s",
        "--fail",
        "--connect-timeout",
        "20",
        "--max-time",
        "60",
        "--retry",
        "3",
        "--retry-all-errors",
        url,
    ]
    for key, value in (headers or {}).items():
        command.extend(["-H", f"{key}: {value}"])
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    return json.loads(fetch_text(url, headers=headers))


def sanitize_wikisource(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n")
    text = re.sub(r"\{\{[^{}]*\}\}\n*", "", text)
    text = re.sub(r"<div[^>]*>", "", text)
    text = re.sub(r"</div>", "", text)
    text = re.sub(r"<br\b[^>]*>", "", text)
    text = re.sub(r"</?span[^>]*>", "", text)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"'''''(.*?)'''''", r"**\1**", text)
    text = re.sub(r"'''(.*?)'''", r"**\1**", text)
    text = re.sub(r"''(.*?)''", r"*\1*", text)
    text = re.sub(r"^=\s*(.*?)\s*=$", r"# \1", text, flags=re.MULTILINE)
    text = re.sub(r"^==\s*(.*?)\s*==$", r"## \1", text, flags=re.MULTILINE)
    text = re.sub(r"^===\s*(.*?)\s*===$", r"### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^[*#:;]+\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def format_kiom_line(item: dict) -> str:
    text = item["original"].strip()
    depth = item["content_level_depth"]
    level = item["content_level"]

    if not text:
        return ""
    if depth == "A" or level == "A":
        return f"### {text}\n"
    if depth in {"B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"} and len(text) <= 120:
        return f"#### {text}\n"
    if depth in {"X", "Y"}:
        return f"{text}\n"
    return f"{text}\n"


def download_kiom_dongui_bogam() -> Path:
    output_path = OUTPUT_DIR / "kiom-dongui-bogam-original.md"
    volume_list = fetch_json(f"{KIOM_API_ROOT}/", headers=KIOM_HEADERS)["DATA"]

    parts: list[str] = [
        "# Dongui Bogam Original Text\n",
        "\n",
        "Source: Korean Institute of Oriental Medicine / Mediclassics raw-text distribution for `동의보감` (`book_id=8`).\n",
        "Attribution: `한의학고전DB(mediclassics.kr)`\n",
        "Usage note: The raw-text distribution page states the files may be used freely for non-commercial purposes with attribution.\n",
        f"Downloaded: {DOWNLOAD_DATE}\n",
        "\n",
        "---\n",
        "\n",
    ]

    for volume in volume_list:
        volume_id = volume["volume_id"]
        volume_name = volume["volume_nm"]
        content_total = volume["content_total"]
        print(f"Downloading KIOM volume {volume_id}: {volume_name}", flush=True)
        parts.append(f"## {volume_name}\n\n")

        for begin in range(1, content_total + 1, 200):
            end = min(begin + 199, content_total)
            url = f"{KIOM_API_ROOT}/{volume_id}/contents?begin={begin}&end={end}"
            chunk = fetch_json(url, headers=KIOM_HEADERS)["DATA"]
            for item in sorted(chunk, key=lambda entry: entry["content_seq"]):
                line = format_kiom_line(item)
                if line:
                    parts.append(line)
            parts.append("\n")
            time.sleep(0.05)

    output_path.write_text("".join(parts), encoding="utf-8")
    return output_path


def download_wikisource_page(filename: str, page_title: str) -> Path:
    encoded_title = urllib.parse.quote(page_title, safe="/")
    raw_url = f"https://ko.wikisource.org/wiki/{encoded_title}?action=raw"
    output_path = OUTPUT_DIR / filename
    print(f"Downloading Wikisource page: {page_title}", flush=True)
    body = sanitize_wikisource(fetch_text(raw_url, headers={"User-Agent": "codex-downloader/1.0"}))

    document = (
        f"# {page_title}\n\n"
        "Source: Korean Wikisource\n"
        f"URL: https://ko.wikisource.org/wiki/{encoded_title}\n"
        "License note: Wikisource content is distributed under the Wikimedia terms and the page-level source status shown by Wikisource.\n"
        f"Downloaded: {DOWNLOAD_DATE}\n\n"
        "---\n\n"
        f"{body}"
    )
    output_path.write_text(document, encoding="utf-8")
    return output_path


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


def build_index(generated_files: list[Path]) -> Path:
    output_path = OUTPUT_DIR / "README.md"
    sorted_files = sorted(generated_files, key=lambda item: item.name)
    file_list = "\n".join(
        (
            f"- [{path.name}](./{path.name})\n"
            f"  - Size: {format_size(path.stat().st_size)}\n"
            f"  - Description: {PAGE_DESCRIPTIONS.get(path.name, 'Downloaded text file.')}"
        )
        for path in sorted_files
    )
    existing_root_file = ROOT / "dongui-bogam-original.md"
    existing_root_note = ""
    if existing_root_file.exists():
        existing_root_note = (
            "\n## Existing Local File\n\n"
            f"- [{existing_root_file.name}](../../{existing_root_file.name})\n"
            "  - Already present in the repo root before this download run.\n"
        )
    content = f"""# Open Korean Medicine Texts

Search date: {DOWNLOAD_DATE}

This directory contains Korean medicine text files that I could copy into the repo without running into the stricter reuse limits on KIOM's translated eBooks. The current collection is centered on `동의보감` because that is where the best combination of openly reusable text, public availability, and machine-readable structure exists.

## Directory Purpose

- Preserve locally usable Markdown copies of openly reusable Korean medicine text.
- Record the search process so future runs do not need to rediscover the same licensing constraints.
- Keep provenance close to the text files themselves.

## How This Folder Was Built

1. Search broadly across Wikisource, Wikibooks, KIOM, and archival sources for Korean medicine texts.
2. Reject sources whose terms did not clearly allow copying the text into this repo.
3. Download the viable text pages as Markdown-compatible plain text.
4. Keep a reproducible script in `scripts/download_korean_medicine_texts.py` so the folder can be refreshed.

## Downloaded

- Korean Wikisource `동의보감` pages
  - Main entry: <https://ko.wikisource.org/wiki/동의보감>
  - Downloaded as cleaned Markdown from the page raw source

Files:
{file_list}
{existing_root_note}

## Official Raw-Text Source

- KIOM `한의학고전DB` raw-text distribution for `동의보감`
  - Source page: <https://info.mediclassics.kr/apps/dist-texts/index.html#/Book/8>
  - Permission shown on the page: free non-commercial use with attribution to `한의학고전DB(mediclassics.kr)`
  - Note: the official API is slow and unstable enough that I did not finish a fresh full 23-volume mirror during this run.
  - The downloader supports an opt-in retry with `python3 scripts/download_korean_medicine_texts.py --include-kiom`

## Searched But Not Copied

- English Wikibooks search for `Korean medicine`, `Han medicine`, and `Dongui Bogam`
  - Result: no relevant book pages found
  - API query used: <https://en.wikibooks.org/w/api.php?action=query&list=search&srsearch=%22Korean%20medicine%22%20OR%20%22Han%20medicine%22%20OR%20%22Dongui%20Bogam%22&format=json>
- Korean Wikibooks search
  - Result: general medicine pages exist, but not an openly editable Korean medicine classic comparable to `동의보감`
  - API query used: <https://ko.wikibooks.org/w/api.php?action=query&list=search&srsearch=동의보감%20OR%20한의학%20OR%20한국%20의학&format=json>
- KIOM Bookshelf free eBooks such as `제세보감` and `방약합편`
  - Source list: <https://info.mediclassics.kr/bookshelf/list/eBook/list>
  - Reason not copied: the terms page says the eBooks are `CC BY-NC-ND 4.0` and explicitly says they should not be reposted online or modified into derivative works
  - Terms: <https://info.mediclassics.kr/bookshelf/terms_of_service>
- Internet Archive search for Korean medicine titles
  - Result: I did not find a reliable, clearly reusable full-text source that was stronger than KIOM raw text or Wikisource

## Reproduction

- Default run: `python3 scripts/download_korean_medicine_texts.py`
- Slower run with attempted official KIOM export: `python3 scripts/download_korean_medicine_texts.py --include-kiom`
- Output directory: `docs/korean-medicine/`

## Caveats

- The Wikisource files are cleaned from raw wiki markup, not hand-edited scholarly editions.
- Some pages mix classical text and modern Korean explanatory material because that is how the Wikisource pages are structured.
- Historical/traditional content should not be treated as current medical guidance.
- The KIOM bookshelf eBooks were intentionally excluded because their terms do not permit reposted derivative Markdown copies.

## Notes

- The official KIOM raw-text distribution remains the strongest machine-readable source for the original text.
- The Wikisource files are useful as an open-source mirror with different editorial formatting.
- These are historical/traditional texts, not current medical guidance.
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path


def build_manifest(generated_files: list[Path]) -> Path:
    output_path = OUTPUT_DIR / "MANIFEST.md"
    rows = []
    for path in sorted(generated_files, key=lambda item: item.name):
        rows.append(
            f"| `{path.name}` | {format_size(path.stat().st_size)} | {PAGE_DESCRIPTIONS.get(path.name, 'Downloaded text file.')} |"
        )
    content = """# Manifest

This manifest summarizes the generated text files in `docs/korean-medicine/`.

| File | Size | Description |
| --- | ---: | --- |
"""
    content += "\n".join(rows) + "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def build_search_notes() -> Path:
    output_path = OUTPUT_DIR / "SEARCH-NOTES.md"
    content = f"""# Search Notes

Search date: {DOWNLOAD_DATE}

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
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-kiom",
        action="store_true",
        help="Attempt the slower official KIOM raw-text export in addition to the Wikisource files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated_files: list[Path] = []
    if args.include_kiom:
        generated_files.append(download_kiom_dongui_bogam())
    for filename, page_title in WIKISOURCE_PAGES:
        generated_files.append(download_wikisource_page(filename, page_title))

    build_index(generated_files)
    build_manifest(generated_files)
    build_search_notes()
    print("Finished generating Markdown files.", flush=True)


if __name__ == "__main__":
    main()
