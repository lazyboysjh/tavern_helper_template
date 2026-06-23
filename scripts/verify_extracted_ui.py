# -*- coding: utf-8 -*-
"""Verify Liangzhu English UI paths and CDN loader references."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = Path(os.environ.get("LIANGZHU_CARD_PATH", ROOT.parents[1] / "梁祝.json"))
SRC = ROOT / "src" / "liangzhu" / "ui"
DIST = ROOT / "dist" / "liangzhu" / "ui"
CDN_PATHS = {
    "cover": "dist/liangzhu/ui/cover/index.html",
    "status": "dist/liangzhu/ui/status/index.html",
    "options_css": "dist/liangzhu/ui/options/styles.css",
    "options_js": "dist/liangzhu/ui/options/controller.js",
}


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    card_text = CARD.read_text(encoding="utf-8")
    card = json.loads(card_text)
    data = card["data"]
    regex = {r["scriptName"]: r for r in data["extensions"]["regex_scripts"]}

    assert_true("dist/梁祝/界面" not in card_text, "card still contains Chinese CDN UI path")
    for label, rel in CDN_PATHS.items():
        assert_true(rel in card_text, f"card missing English CDN path for {label}: {rel}")

    files = [
        SRC / "cover" / "index.html",
        SRC / "cover" / "index.ts",
        SRC / "status" / "index.html",
        SRC / "status" / "index.ts",
        SRC / "options" / "index.html",
        SRC / "options" / "index.ts",
        SRC / "options" / "styles.css",
        SRC / "options" / "controller.js",
        DIST / "cover" / "index.html",
        DIST / "cover" / "index.js",
        DIST / "status" / "index.html",
        DIST / "status" / "index.js",
        DIST / "options" / "index.html",
        DIST / "options" / "index.js",
        DIST / "options" / "styles.css",
        DIST / "options" / "controller.js",
    ]
    for file in files:
        assert_true(file.exists(), f"missing file: {file}")
        print(f"OK exists: {file.relative_to(ROOT)}")

    status_loader = regex["显示-状态栏美化"]["replaceString"]
    options_loader = regex["显示-行动选项栏美化"]["replaceString"]
    assert_true("dist/liangzhu/ui/status/index.html" in status_loader, "status loader not English path")
    assert_true("dist/liangzhu/ui/options/styles.css" in options_loader, "options CSS loader not English path")
    assert_true("dist/liangzhu/ui/options/controller.js" in options_loader, "options JS loader not English path")
    assert_true("dist/liangzhu/ui/cover/index.html" in data["first_mes"], "cover loader not English path")

    src_status = (SRC / "status" / "index.html").read_text(encoding="utf-8")
    src_cover = (SRC / "cover" / "index.html").read_text(encoding="utf-8")
    src_options = (SRC / "options" / "index.html").read_text(encoding="utf-8")
    assert_true("CHAR_ORDER" in src_status, "status source missing CHAR_ORDER")
    assert_true("按足始知女儿身" in src_cover, "cover source missing title")
    assert_true("mnx-opts-wrap" in src_options, "options source missing wrapper")

    print("RESULT: English Liangzhu UI path verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
