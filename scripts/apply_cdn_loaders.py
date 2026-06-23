# -*- coding: utf-8 -*-
"""Update 梁祝.json to CDN loaders; split options CSS/JS for $1 shell."""
import json
import os
import re
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1]
CARD_PATH = Path(os.environ.get("LIANGZHU_CARD_PATH", TEMPLATE.parents[1] / "梁祝.json"))
CDN = "https://testingcf.jsdelivr.net/gh/lazyboysjh/tavern_helper_template@main/dist/liangzhu/ui"
V = "?v=1"

STATUS_SHELL = f"""```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
</head>
<body style="margin:0;padding:0;background:transparent;">
<script>
$('body').load('{CDN}/status/index.html{V}');
</script>
</body>
</html>
```"""

COVER_SHELL = f"""```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
</head>
<body style="margin:0;padding:0;background:transparent;">
<script>
$('body').load('{CDN}/cover/index.html{V}');
</script>
</body>
</html>
```"""

OPTIONS_SHELL = f"""```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>梁祝行动选项</title>
<link rel="stylesheet" href="{CDN}/options/styles.css{V}">
</head>
<body style="margin:0;padding:0;background:transparent;">
<div class="mnx-opts-wrap" data-mnx-inline="1">
<div class="mnx-opts-head"><span class="mnx-opts-head-core"><span class="mnx-opts-title">行动抉择</span><button type="button" class="mnx-mode-btn">直接发送</button></span></div>
$1
</div>
<script src="{CDN}/options/controller.js{V}"></script>
</body>
</html>
```"""


def split_options(html: str):
    m = re.search(r"<style>([\s\S]*?)</style>", html)
    if not m:
        raise SystemExit("options: no style block")
    css = m.group(1).strip()
    m2 = re.search(r"<div class=\"mnx-opts-wrap\"[^>]*>\s*<div class=\"mnx-opts-head\">[\s\S]*?</div>\$1<script>([\s\S]*?)</script>", html)
    if not m2:
        raise SystemExit("options: no controller script block")
    js = m2.group(1).strip()
    return css, js


def main():
    opt_html = (TEMPLATE / "src/liangzhu/ui/options/index.html").read_text(encoding="utf-8")
    css, js = split_options(opt_html)
    out = TEMPLATE / "src/liangzhu/ui/options"
    (out / "styles.css").write_text(css + "\n", encoding="utf-8")
    (out / "controller.js").write_text(js + "\n", encoding="utf-8")
    print(f"Wrote styles.css ({len(css)} chars)")
    print(f"Wrote controller.js ({len(js)} chars)")

    card = json.loads(CARD_PATH.read_text(encoding="utf-8"))
    data = card["data"]
    data["first_mes"] = COVER_SHELL
    for r in data["extensions"]["regex_scripts"]:
        if r["scriptName"] == "显示-状态栏美化":
            r["replaceString"] = STATUS_SHELL
        elif r["scriptName"] == "显示-行动选项栏美化":
            r["replaceString"] = OPTIONS_SHELL

    CARD_PATH.write_text(json.dumps(card, ensure_ascii=False, indent=4), encoding="utf-8")
    print("Updated 梁祝.json: first_mes, 状态栏, 行动选项")
    print("Status shell len:", len(STATUS_SHELL))
    print("Options shell len:", len(OPTIONS_SHELL))


if __name__ == "__main__":
    main()
