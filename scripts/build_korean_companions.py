#!/usr/bin/env python3
"""Build Korean companion Markdown files from app.mediclassics.kr Korean text."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "korean-medicine"
CACHE_DIR = ROOT / ".cache"
DOWNLOAD_DATE = "2026-03-12"
BASE_URL = "https://app.mediclassics.kr/books/%EB%8F%99%EC%9D%98%EB%B3%B4%EA%B0%90/pages"
USER_AGENT = "codex-korean-companion/1.0"
STATE_FILE = CACHE_DIR / "korean-companion-state.json"


SECTIONS = [
    {
        "source_file": "dongui-bogam-seomun.md",
        "output_file": "dongui-bogam-seomun-ko.md",
        "title": "동의보감/서문 한국어본",
        "page_range": (1, 1),
        "description": "Official Korean translation from app.mediclassics.kr page 1.",
    },
    {
        "source_file": "dongui-bogam-jibrye.md",
        "output_file": "dongui-bogam-jibrye-ko.md",
        "title": "동의보감/집례 한국어본",
        "page_range": (3, 4),
        "description": "Official Korean translation from app.mediclassics.kr pages 3-4.",
    },
    {
        "source_file": "dongui-bogam-naegyeongpyeon.md",
        "output_file": "dongui-bogam-naegyeongpyeon-ko.md",
        "title": "동의보감/내경편 한국어본",
        "page_range": (5, 524),
        "description": "Official Korean translation from app.mediclassics.kr pages 5-524.",
    },
    {
        "source_file": "dongui-bogam-oehyeongpyeon.md",
        "output_file": "dongui-bogam-oehyeongpyeon-ko.md",
        "title": "동의보감/외형편 한국어본",
        "page_range": (525, 1060),
        "description": "Official Korean translation from app.mediclassics.kr pages 525-1060.",
    },
    {
        "source_file": "dongui-bogam-japbyeongpyeon.md",
        "output_file": "dongui-bogam-japbyeongpyeon-ko.md",
        "title": "동의보감/잡병편 한국어본",
        "page_range": (1061, 2048),
        "description": "Official Korean translation from app.mediclassics.kr pages 1061-2048.",
    },
    {
        "source_file": "dongui-bogam-chimgupyeon.md",
        "output_file": "dongui-bogam-chimgupyeon-ko.md",
        "title": "동의보감/침구편 한국어본",
        "page_range": (2796, 2888),
        "description": "Official Korean translation from app.mediclassics.kr pages 2796-2888.",
    },
]


def run_curl(url: str) -> str:
    command = [
        "curl",
        "--http1.1",
        "-L",
        "-s",
        "--fail",
        "--connect-timeout",
        "20",
        "--max-time",
        "120",
        "--retry",
        "3",
        "--retry-all-errors",
        "-H",
        f"User-Agent: {USER_AGENT}",
        url,
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout


def html_to_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def extract_ko_paragraphs(page_html: str) -> list[str]:
    bottom_match = re.search(
        r'<div class="body container bottom">(.*?)(?:<script src=|</body>)',
        page_html,
        flags=re.DOTALL,
    )
    bottom = bottom_match.group(1) if bottom_match else page_html
    paragraphs = re.findall(
        r'<p class="KO"[^>]*>(.*?)</p>',
        bottom,
        flags=re.DOTALL,
    )
    result = []
    for paragraph in paragraphs:
        text = html_to_text(paragraph)
        if text:
            result.append(text)
    return result


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_page(page_number: int) -> tuple[int, list[str]]:
    html = run_curl(f"{BASE_URL}/{page_number}")
    return page_number, extract_ko_paragraphs(html)


def build_section(section: dict, state: dict) -> Path:
    output_path = SOURCE_DIR / section["output_file"]
    start_page, end_page = section["page_range"]
    state_key = section["output_file"]
    cache = state.get(state_key, {})

    missing_pages = [
        page_number
        for page_number in range(start_page, end_page + 1)
        if str(page_number) not in cache
    ]

    if missing_pages:
        print(
            f"Fetching {section['output_file']} pages {start_page}-{end_page} "
            f"({len(missing_pages)} missing)",
            flush=True,
        )
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(fetch_page, page_number): page_number for page_number in missing_pages}
            for future in as_completed(futures):
                page_number, paragraphs = future.result()
                cache[str(page_number)] = paragraphs
                if page_number % 50 == 0 or page_number in {start_page, end_page}:
                    print(f"  page {page_number} done", flush=True)
                state[state_key] = cache
                save_state(state)

    parts = [
        f"# {section['title']}\n\n",
        "Source: app.mediclassics.kr official Korean translation layer\n",
        f"URL range: {BASE_URL}/{start_page} - {BASE_URL}/{end_page}\n",
        f"Based on original file: {section['source_file']}\n",
        f"Description: {section['description']}\n",
        f"Downloaded: {DOWNLOAD_DATE}\n\n",
        "---\n\n",
    ]

    for page_number in range(start_page, end_page + 1):
        paragraphs = cache.get(str(page_number), [])
        if not paragraphs:
            continue
        parts.append(f"## Page {page_number}\n\n")
        for paragraph in paragraphs:
            parts.append(paragraph)
            parts.append("\n\n")

    output_path.write_text("".join(parts), encoding="utf-8")
    state[state_key] = cache
    save_state(state)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        nargs="*",
        help="Optional list of output filenames to build, for example dongui-bogam-seomun-ko.md",
    )
    args = parser.parse_args()

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    generated = []
    selected_sections = SECTIONS
    if args.only:
        allowed = set(args.only)
        selected_sections = [section for section in SECTIONS if section["output_file"] in allowed]
    for section in selected_sections:
        generated.append(build_section(section, state))
    print(f"Built {len(generated)} Korean companion files.", flush=True)


if __name__ == "__main__":
    main()
