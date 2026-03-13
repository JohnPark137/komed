from __future__ import annotations

import html
import re
import sys
from pathlib import Path


def main() -> None:
    page_no = sys.argv[1]
    out_path = Path(sys.argv[2])
    raw_html = sys.stdin.read()

    items = re.findall(r'<p class="KO"[^>]*>(.*?)</p>', raw_html, re.S)
    chunks: list[str] = []

    for item in items:
        item = re.sub(r"<br\s*/?>", "\n", item)
        item = re.sub(r"<[^>]+>", "", item)
        item = html.unescape(item)
        item = re.sub(r"[ \t]+", " ", item)
        item = re.sub(r"\n{2,}", "\n", item)
        item = item.strip()
        if item:
            chunks.append(item)

    if not chunks:
        out_path.write_text("", encoding="utf-8")
        return

    text = f"## Page {page_no}\n\n" + "\n\n".join(chunks) + "\n"
    out_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
