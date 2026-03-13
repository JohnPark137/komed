from __future__ import annotations

import re
import sys
from pathlib import Path

from pypdf import PdfReader


PDFS = [
    "Dongui-Bogam.pdf",
    "Dongui-Bogam-Index.pdf",
    "jesebogam.pdf",
    "chimgugeukbijeon.pdf",
    "bangyakhappyeon-vol1.pdf",
]


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = text.replace("\t", " ")
    text = text.replace("\r", "\n")
    lines = [re.sub(r"[ ]{2,}", " ", line).strip() for line in text.splitlines()]

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


def convert_pdf(pdf_path: Path) -> Path:
    reader = PdfReader(str(pdf_path))
    md_path = pdf_path.with_suffix(".md")

    title = pdf_path.stem.replace("-", " ")
    parts = [f"# {title}", "", f"Source PDF: `{pdf_path.name}`", f"Pages: {len(reader.pages)}", ""]

    for index, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        text = normalize_text(raw_text)
        if not text:
            continue

        parts.append(f"## Page {index}")
        parts.append("")
        parts.append(text)
        parts.append("")

    md_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return md_path


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    targets = sys.argv[1:] or PDFS
    for name in targets:
        pdf_path = root / name
        if not pdf_path.exists():
            continue
        md_path = convert_pdf(pdf_path)
        print(md_path.name, flush=True)


if __name__ == "__main__":
    main()
