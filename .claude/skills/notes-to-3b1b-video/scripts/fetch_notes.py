"""Turn course notes into clean Markdown files, without a model reading them.

The coordinator runs this and reads only its summary table; the author reads the files.

Sources:
  URL   a page of a course-notes site. When the page links to its source on GitHub
        ("edit" link), the Markdown source is used, and with it every page of the
        same folder in the site's table of contents (myst.yml / _toc.yml), in order.
        Otherwise the page's main text is extracted from the HTML.
  .pdf  every page rendered to pages/*.png and its text layer kept; the pages are
        listed in batches in TRANSCRIBE.md for the transcriber role (a vision model
        reads the images: text, math, tables, figures). Then `--verify` compares each
        transcribed page with the PDF's own text layer and rebuilds INDEX.md.
        Needs `pip install pypdfium2`.
  .md / .html   local files, cleaned the same way.

Output in OUT: NN-<name>.md per page, images/ with the figures the notes use,
INDEX.md (title, group, words, figures, tables per file). Cite notes as
`notes/NN-name.md:LINE`.

Usage:
    python fetch_notes.py https://notes.cs61c.org/content/datapath/ --out cs61c/datapath/notes
    python fetch_notes.py lecture.pdf notes.md --out U/notes
    python fetch_notes.py --out U/notes --verify          # after the transcribers
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (notes-to-3b1b-video fetch_notes)"}


def get(url: str, binary=False):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    return data if binary else data.decode("utf-8", errors="replace")


# ---------------------------------------------------------------- MyST / Markdown

FENCE = re.compile(r"^(\s*)(:{3,}|`{3,})\{([\w-]+)\}\s*(.*)$")
OPTION = re.compile(r"^\s*:([\w-]+):\s*(.*)$")
DROP = {"iframe", "youtube", "video", "raw", "embed"}


def _parse(lines, i, close):
    """Nodes until the closing fence `close` (None: end of file)."""
    nodes = []
    while i < len(lines):
        line = lines[i]
        if close is not None and line.strip() == close:
            return nodes, i + 1
        m = FENCE.match(line)
        if m:
            fence, kind, arg = m[2], m[3], m[4].strip()
            opts, i = {}, i + 1
            while i < len(lines) and OPTION.match(lines[i]):
                k, v = OPTION.match(lines[i]).groups()
                opts[k] = v.strip().strip('"')
                i += 1
            body, i = _parse(lines, i, fence)
            nodes.append(("dir", kind, arg, opts, body))
            continue
        nodes.append(("line", line))
        i += 1
    return nodes, i


def _has(nodes, kinds):
    return any(n[0] == "dir" and (n[1] in kinds or _has(n[4], kinds)) for n in nodes)


def _text(nodes):
    return " ".join(n[1].strip() for n in nodes if n[0] == "line" and n[1].strip())


def _render(nodes, figs, out):
    for n in nodes:
        if n[0] == "line":
            if not re.match(r"^\s*:{3,}\s*$", n[1]):   # an unmatched closing fence
                out.append(n[1])
            continue
        _, kind, arg, opts, body = n
        if kind in DROP or _has(body, DROP) or "🎥" in arg:
            continue
        label = f" ({opts['label']})" if "label" in opts else ""
        if kind == "figure":
            if arg.startswith("#"):        # a reference to another figure, not an image
                arg = ""
            else:
                figs.append(arg)
            alt = opts.get("alt", "")
            out += ["", f"**Figure{label}** ![{alt}]({'images/' + Path(arg).name if arg else ''})",
                    _text(body), ""]
        elif kind in ("image",):
            figs.append(arg)
            out += [f"![{opts.get('alt', '')}](images/{Path(arg).name})"]
        elif kind in ("math",):
            out += ["$$", *[x[1] for x in body if x[0] == "line"], "$$"]
        elif kind in ("code", "code-block", "code-cell"):
            out += [f"```{arg}", *[x[1] for x in body if x[0] == "line"], "```"]
        elif kind == "table":
            out += ["", f"**Table{label}: {arg}**"]
            _render(body, figs, out)
        else:   # note, tip, warning, admonition, dropdown, card, tab-item, ...
            title = arg or kind
            out += ["", f"**{kind.capitalize()}: {title}**" if arg else f"**{kind.capitalize()}**"]
            _render(body, figs, out)
            out.append("")


def inline(s: str) -> str:
    s = re.sub(r"\{(?:term|abbr|sub|sup|strong|emphasis|index|kbd|code)\}`([^`]*)`", r"\1", s)
    s = re.sub(r"\{(?:math|eq)\}`([^`]*)`", r"$\1$", s)
    s = re.sub(r"\{(?:ref|numref|doc|download)\}`([^`<]*?)\s*(?:<[^>]*>)?`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\(#[^)]*\)", r"\1", s)                   # internal links → text
    s = re.sub(r"\[([^\]]+)\]\((/[^)]*)\)", r"\1", s)                  # site-relative links → text
    s = re.sub(r"(?<![\w\[])@((?:fig|tab|eq|sec)-[\w-]+)", r"(\1)", s)  # @fig-x → (fig-x)
    return s


def clean_markdown(text: str):
    """(title, cleaned markdown, figure paths) of a MyST or plain Markdown page."""
    title = ""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        t = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", m[1], re.M)
        title = t[1] if t else ""
        text = text[m.end():]
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)                # commented-out blocks
    lines = [x for x in text.splitlines() if not re.match(r"^\s*\([\w:.-]+\)=\s*$", x)
             and not re.match(r"^\s*%", x)]                           # MyST labels and comments
    nodes, _ = _parse(lines, 0, None)
    out, figs = [], []
    _render(nodes, figs, out)
    body = "\n".join(inline(x).rstrip() for x in out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    if title and not body.startswith("# "):
        body = f"# {title}\n\n{body}"
    return title, body, figs


# ---------------------------------------------------------------- HTML

def html_to_markdown(html: str, base: str):
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("article") or soup.find("main") or soup.body
    for t in root.find_all(["nav", "aside", "script", "style", "header", "footer", "iframe", "button", "form"]):
        t.decompose()
    for a in root.select("a.headerlink, .headerlink"):
        a.decompose()
    out, figs = [], []

    def txt(el):
        s = el.get_text(" ", strip=True) if not isinstance(el, NavigableString) else str(el).strip()
        return re.sub(r"\s+", " ", s.replace("¶", "")).strip()

    def walk(el):
        for c in el.children:
            if isinstance(c, NavigableString):
                continue
            name = c.name
            if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                out += ["", "#" * int(name[1]) + " " + re.sub(r"^\d+(\.\d+)*\s*", "", txt(c)), ""]
            elif name == "p":
                out += [txt(c), ""]
            elif name in ("ul", "ol"):
                for k, li in enumerate(c.find_all("li", recursive=False)):
                    out.append(("- " if name == "ul" else f"{k + 1}. ") + txt(li))
                out.append("")
            elif name == "pre":
                out += ["```", c.get_text().rstrip(), "```", ""]
            elif name == "table":
                rows = [[txt(td) for td in tr.find_all(["td", "th"])] for tr in c.find_all("tr")]
                if rows:
                    out.append("| " + " | ".join(rows[0]) + " |")
                    out.append("|" + "---|" * len(rows[0]))
                    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                    out.append("")
            elif name == "img":
                src = urllib.parse.urljoin(base, c.get("src", ""))
                figs.append(src)
                out += [f"![{c.get('alt', '')}](images/{Path(urllib.parse.urlparse(src).path).name})", ""]
            elif name == "figcaption":
                out += [f"*{txt(c)}*", ""]
            else:
                walk(c)

    walk(root)
    title = txt(soup.find("h1")) if soup.find("h1") else (soup.title.get_text() if soup.title else "")
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    return title, body, figs


# ---------------------------------------------------------------- sources

def github_pages(html: str):
    """[(raw url, path, group)] for every page in the edited page's folder, in toc order."""
    m = re.search(r"https://github\.com/([\w.-]+)/([\w.-]+)/edit/([\w.-]+)/([^\"'#?]+\.md)", html)
    if not m:
        return None
    owner, repo, branch, path = m.groups()
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
    folder = path.rsplit("/", 1)[0] + "/"
    for toc in ("myst.yml", "_toc.yml"):
        try:
            text = get(raw + toc)
        except Exception:
            continue
        pages, group = [], ""
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                continue
            t = re.match(r"\s*-?\s*title:\s*[\"']?(.*?)[\"']?\s*$", line)
            if t:
                group = t[1]
            f = re.match(r"\s*-?\s*file:\s*(\S+)", line)
            if f and f[1].startswith(folder):
                p = f[1] if f[1].endswith(".md") else f[1] + ".md"
                pages.append((raw + p, p, group))
        if pages:
            return pages
    api = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder.rstrip('/')}?ref={branch}"
    names = sorted(x["name"] for x in json.loads(get(api)) if x["name"].endswith(".md"))
    names.sort(key=lambda n: n != "index.md")
    return [(raw + folder + n, folder + n, "") for n in names]


BATCH = 6     # PDF pages per transcriber batch
AGREE = 0.85  # share of a page's text-layer words a transcript must contain


def pdf_prepare(path: Path, out: Path, first: int):
    """Render each page to a PNG and keep its text layer; write the transcriber's task list.
    Returns the batches: (output file name, [page numbers])."""
    import pypdfium2 as pdfium
    (out / "pages").mkdir(exist_ok=True)
    (out / ".text").mkdir(exist_ok=True)
    stem = re.sub(r"[^\w-]+", "-", path.stem).strip("-")
    pdf = pdfium.PdfDocument(str(path))
    for k in range(len(pdf)):
        page = pdf[k]
        page.render(scale=150 / 72).to_pil().save(out / "pages" / f"{stem}-p{k + 1:03d}.png")
        (out / ".text" / f"{stem}-p{k + 1:03d}.txt").write_text(page.get_textpage().get_text_range(),
                                                                encoding="utf-8")
    n = len(pdf)
    return [(f"{first + i:02d}-{stem}-p{a:03d}-{min(a + BATCH - 1, n):03d}.md",
             list(range(a, min(a + BATCH, n + 1))), stem)
            for i, a in enumerate(range(1, n + 1, BATCH))]


def _words(s: str) -> set:
    return set(re.findall(r"[a-z]{3,}", s.lower()))


def verify(out: Path) -> list[str]:
    """Pages whose transcript misses much of the PDF's own text layer."""
    flags = []
    for f in sorted(out.glob("[0-9][0-9]-*.md")):
        parts = re.split(r"^<!-- page (\d+) -->\s*$", f.read_text(encoding="utf-8"), flags=re.M)
        m = re.match(r"\d\d-(.+)-p\d{3}-\d{3}\.md$", f.name)
        if not m:
            continue
        for num, text in zip(parts[1::2], parts[2::2]):
            layer = out / ".text" / f"{m[1]}-p{int(num):03d}.txt"
            ref = _words(layer.read_text(encoding="utf-8")) if layer.exists() else set()
            if len(ref) < 15:
                continue   # scanned or a figure page: nothing to compare with
            got = len(ref & _words(text)) / len(ref)
            if got < AGREE:
                flags.append(f"{f.name} page {num}: {got:.0%} of the text layer's words")
    return flags


def residue(body: str) -> int:
    """Lines that still look like markup a reader should not see."""
    return sum(1 for x in body.splitlines()
               if re.match(r"^\s*(:{3,}|\{[\w-]+\}|:[\w-]+:\s)", x) or "¶" in x or "{term}" in x)


def write_index(out: Path) -> tuple[list[str], int, int]:
    meta = json.loads((out / ".meta.json").read_text(encoding="utf-8")) if (out / ".meta.json").exists() else {}
    head = ["| file | title | group | words | figures | tables | lines | residue | note |",
            "|---|---|---|---|---|---|---|---|---|"]
    rows, total, bad = [], 0, 0
    for name, m in meta.items():
        f = out / name
        if not f.exists():
            rows.append(f"| {name} | {m['title'] or '—'} | {m['group'] or '—'} | — | — | — | — | | to transcribe |")
            continue
        body = f.read_text(encoding="utf-8")
        words, r = len(body.split()), residue(body)
        total, bad = total + words, bad + r
        tables = len(re.findall(r"^\|\s*:?-{2,}", body, re.M))
        rows.append(f"| {name} | {m['title'] or '—'} | {m['group'] or '—'} | {words} | {m['figs']} | {tables} | "
                    f"{body.count(chr(10))} | {r or ''} | {m['note']} |")
    (out / "INDEX.md").write_text("# Notes\n\n" + "\n".join(head + rows) + f"\n\nTotal {total} words "
                                  f"(~{int(total * 1.4)} tokens). Cite as `notes/<file>:LINE`. PDF page images: "
                                  "`pages/`; figures: `images/`.\n", encoding="utf-8")
    return head + rows, total, bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sources", nargs="*")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-images", action="store_true")
    ap.add_argument("--verify", action="store_true", help="after transcription: cross-check and rebuild INDEX.md")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(a.out)
    (out / "images").mkdir(parents=True, exist_ok=True)
    if a.verify:
        table, total, bad = write_index(out)
        flags = verify(out)
        todo = [r for r in table if r.endswith("to transcribe |")]
        print("\n".join(table))
        print(f"\n{total} words; {len(todo)} files still to transcribe; "
              + ("; ".join(flags) + ": have those pages checked against their images" if flags else "transcripts agree with the text layer"))
        return

    docs, batches = [], []   # docs: (name, title, group, body, figure urls, note)
    for src in a.sources:
        if re.match(r"https?://", src):
            html = get(src)
            pages = github_pages(html)
            if pages:
                for url, path, group in pages:
                    title, body, figs = clean_markdown(get(url))
                    base = url.rsplit("/", 1)[0] + "/"
                    docs.append((Path(path).stem, title, group, body,
                                 [urllib.parse.urljoin(base, f) for f in figs if f], f"source {path}"))
            else:
                title, body, figs = html_to_markdown(html, src)
                docs.append((Path(urllib.parse.urlparse(src).path.rstrip("/")).name or "page",
                             title, "", body, figs, "from HTML"))
        else:
            p = Path(src)
            if p.suffix.lower() == ".pdf":
                docs.append(("pdf", p, "", "", [], ""))   # placeholder, prepared below in order
            elif p.suffix.lower() in (".html", ".htm"):
                title, body, figs = html_to_markdown(p.read_text(encoding="utf-8"), p.as_uri())
                docs.append((p.stem, title, "", body, figs, "from HTML"))
            else:
                title, body, figs = clean_markdown(p.read_text(encoding="utf-8"))
                docs.append((p.stem, title, "", body, [], "local"))

    meta, k = {}, 1
    for name, title, group, body, figs, note in docs:
        if name == "pdf":   # page images + text layer now; the transcriber writes the files
            for fname, pages, stem in pdf_prepare(title, out, k):
                meta[fname] = {"title": f"{stem}, pages {pages[0]}–{pages[-1]}", "group": stem,
                               "figs": "page images", "note": "transcribed from page images"}
                batches.append((fname, pages, stem))
                k += 1
            continue
        fname = f"{k:02d}-{re.sub(r'[^\w-]+', '-', name).strip('-')}.md"
        k += 1
        (out / fname).write_text(body, encoding="utf-8")
        got = 0
        if not a.no_images:
            for f in figs:
                try:
                    (out / "images" / Path(urllib.parse.urlparse(f).path).name).write_bytes(get(f, binary=True))
                    got += 1
                except Exception:
                    pass
        meta[fname] = {"title": title, "group": group, "figs": f"{got}/{len(figs)}", "note": note}
    (out / ".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if batches:
        (out / "TRANSCRIBE.md").write_text(
            "# Transcription tasks (assets/roles/transcriber.md)\n\n| output | pages | images |\n|---|---|---|\n"
            + "\n".join(f"| {f} | {p[0]}–{p[-1]} | pages/{s}-p{p[0]:03d}.png … pages/{s}-p{p[-1]:03d}.png |"
                        for f, p, s in batches) + "\n", encoding="utf-8")
    table, total, bad = write_index(out)
    print("\n".join(table))
    print(f"\n{len(meta)} files, {total} words (~{int(total * 1.4)} tokens) in {out}"
          + (f"; {bad} lines of markup residue: have a small model clean those files" if bad else "")
          + (f"; {len(batches)} PDF batches in TRANSCRIBE.md: one transcriber per batch, then --verify"
             if batches else ""))


if __name__ == "__main__":
    main()
