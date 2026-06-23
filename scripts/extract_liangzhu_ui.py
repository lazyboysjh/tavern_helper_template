# -*- coding: utf-8 -*-
"""Extract 梁祝 cover/status/options HTML from 梁祝.json into English src paths."""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = Path(os.environ.get("LIANGZHU_CARD_PATH", ROOT.parents[1] / "梁祝.json"))
SRC = ROOT / "src" / "liangzhu" / "ui"
UI_PATHS = {
    "封面": "cover",
    "状态栏": "status",
    "行动选项": "options",
}

STUB_TS = """// Legacy self-contained UI entry (webpack stub).
// All markup/scripts live in index.html beside this file.
export {};
"""


def strip_html_fence(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```html\s*([\s\S]*?)\s*```$", text, re.I)
    if m:
        return m.group(1).strip()
    return text


def assert_embedded_ui(name: str, html: str) -> None:
    if "testingcf.jsdelivr.net/gh/lazyboysjh/tavern_helper_template" in html:
        raise SystemExit(
            f"{name}: card contains a CDN loader, not embedded UI. "
            "Use src/liangzhu/ui as the source of truth and run apply_cdn_loaders.py instead."
        )


def main():
    data = json.loads(CARD.read_text(encoding="utf-8"))["data"]
    regex = {r["scriptName"]: r for r in data["extensions"]["regex_scripts"]}

    items = [
        ("封面", data.get("first_mes", "")),
        ("状态栏", regex["显示-状态栏美化"]["replaceString"]),
        ("行动选项", regex["显示-行动选项栏美化"]["replaceString"]),
    ]

    for name, raw in items:
        html = strip_html_fence(raw)
        if not html.lower().startswith("<!doctype"):
            raise SystemExit(f"{name}: expected full HTML document")
        assert_embedded_ui(name, html)
        out = SRC / UI_PATHS[name]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(html, encoding="utf-8")
        (out / "index.ts").write_text(STUB_TS, encoding="utf-8")
        print(f"OK {name}: {len(html)} chars -> {out}")

    print("Done.")


if __name__ == "__main__":
    main()
