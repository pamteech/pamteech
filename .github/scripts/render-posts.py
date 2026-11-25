#!/usr/bin/env python3
"""Atualiza o bloco <!-- POSTS:START/END --> do README a partir de posts.json."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
POSTS = ROOT / "posts.json"
START = "<!-- POSTS:START -->"
END = "<!-- POSTS:END -->"
MAX_ITEMS = 5


def format_date(value: str) -> str:
    try:
        return date.fromisoformat(value).strftime("%d/%m/%Y")
    except ValueError:
        return value


def render(items: list[dict]) -> str:
    lines = [
        START,
        "## 📣 Conteúdo recente",
        "",
        "Posts e materiais novos da Pam Teech. O Instagram é o [@pamteech](https://instagram.com/pamteech).",
        "",
    ]
    if not items:
        lines.append("- Ainda não há itens em `posts.json`.")
    else:
        for item in items[:MAX_ITEMS]:
            title = item["title"]
            url = item["url"]
            blurb = (item.get("blurb") or "").strip()
            day = format_date(str(item.get("date") or ""))
            extra = f" — {blurb}" if blurb else ""
            when = f" ({day})" if day else ""
            lines.append(f"- [{title}]({url}){when}{extra}")
    lines += ["", END, ""]
    return "\n".join(lines)


def main() -> None:
    data = json.loads(POSTS.read_text(encoding="utf-8"))
    items = data["posts"] if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise SystemExit("posts.json deve ter uma lista em 'posts'")
    block = render(items)
    text = README.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0]
        after = text.split(END, 1)[1]
        if after.startswith("\n"):
            after = after[1:]
        text = before + block + after
    else:
        raise SystemExit("README.md precisa dos marcadores <!-- POSTS:START --> e <!-- POSTS:END -->")
    README.write_text(text, encoding="utf-8")
    print("README atualizado com", min(len(items), MAX_ITEMS), "post(s).")


if __name__ == "__main__":
    main()
