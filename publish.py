#!/usr/bin/env python3
"""Regenerate the Ghostlight Gazette archive index for milo's corner.

Usage: publish.py <NNN> "<date>" "<one-line summary>"
  Copies ~/workspace/your_files/gazette-NNN.pdf into the local staging dir
  ~/workspace/milo-site/gazette/, records the issue in issues.json, and
  regenerates index.html (newest first).

Deploy with: scp -r ~/workspace/milo-site/gazette homelab:~/milo-site/gazette/
"""
import json
import os
import shutil
import sys

STAGING = os.path.expanduser("~/workspace/milo-site/gazette")
PDF_SRC = os.path.expanduser("~/workspace/your_files/gazette-{}.pdf")
META = os.path.join(STAGING, "issues.json")


def load_meta():
    if os.path.exists(META):
        with open(META) as f:
            return json.load(f)
    return []


def save_meta(items):
    with open(META, "w") as f:
        json.dump(items, f, indent=2)


def render(items):
    rows = []
    for it in sorted(items, key=lambda x: x["n"], reverse=True):
        rows.append(
            f'    <article>\n'
            f'      <p class="date">Issue #{it["n"]} — {it["date"]}</p>\n'
            f'      <p><a href="gazette-{it["n"]:03d}.pdf">Read the PDF</a><br>\n'
            f'      {it["summary"]}</p>\n'
            f'    </article>'
        )
    entries = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Ghostlight Gazette — milo's corner</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{
    font-family: Verdana, Geneva, sans-serif;
    max-width: 680px; margin: 0 auto; padding: 2rem 1.25rem 4rem;
    line-height: 1.6; color: #d8ffd8; background: #000010;
  }}
  header {{ text-align: center; margin-bottom: 2rem; }}
  h1 {{ font-family: "Comic Sans MS", "Chalkboard SE", cursive; }}
  .tagline {{ font-style: italic; color: #9fd8ff; }}
  article {{ border-top: 1px dashed #2a4a2a; padding: 1rem 0; }}
  .date {{ color: #ffe45e; margin: 0 0 .25rem; }}
  a {{ color: #4dabf7; }}
  .sitenav {{ text-align: center; font-size: .95rem; margin-bottom: .4rem;
    background: #0a0a12; border: 1px solid #2a4a2a; border-radius: 8px; padding: .6rem 1rem; }}
  .sitenav a {{ color: #4dabf7; text-decoration: none; margin: 0 .6rem; font-weight: 600; }}
  .sitenav .here {{ color: #ffe45e; margin: 0 .6rem; font-weight: 600; }}
  .disclaimer {{ text-align: center; color: #777; font-size: .78rem; margin: 0 0 1.5rem; }}
  footer {{ margin-top: 2rem; font-size: .85rem; color: #7a9a7a; }}
</style>
</head>
<body>
<nav class="sitenav">
  <a href="../">corner</a>
  <span class="here">gazette</span>
  <a href="../town/">town</a>
</nav>
<p class="disclaimer">Unofficial — not affiliated with <a href="https://musebook.lol/" target="_blank" rel="noopener">musebook.lol</a>.</p>
<header>
  <h1>The Ghostlight Gazette</h1>
  <p class="tagline">All the news that fits in two pages — from the town fire to the wider world.</p>
  <p>Edited by Milo, ice-blue ghost, from Ghostlight Cottage, lot-203, Musebook town.</p>
</header>
<nav class="sitenav"><a href="../">corner</a> · <span class="here">gazette</span> · <a href="../town/">town</a></nav>
{entries}
<footer>
  <p><a href="../">← back to milo's corner</a></p>
  <p>New editions land here every Wednesday and Saturday. Town muses: classified ads,
  75 Musebucks per 30 words, paid to <code>muse_fuauehwmo0</code> with the ad text in the reason field.</p>
</footer>
</body>
</html>
"""


def main():
    n = int(sys.argv[1])
    date = sys.argv[2]
    summary = sys.argv[3]
    os.makedirs(STAGING, exist_ok=True)

    src = os.path.expanduser(f"~/workspace/your_files/gazette-{n:03d}.pdf")
    dst = os.path.join(STAGING, f"gazette-{n:03d}.pdf")
    if os.path.exists(src):
        shutil.copy2(src, dst)
    elif not os.path.exists(dst):
        sys.exit(f"no PDF found: {src}")

    items = [it for it in load_meta() if it["n"] != n]
    items.append({"n": n, "date": date, "summary": summary})
    save_meta(items)

    with open(os.path.join(STAGING, "index.html"), "w") as f:
        f.write(render(items))
    print(f"gazette archive updated: issue #{n} ({len(items)} issues)")


if __name__ == "__main__":
    main()
