#!/usr/bin/env python3
"""Lint the internal docs: links, removed names, code-coupling hints, decision provenance.

Usage: python tools/doclint.py [files...] | --self-test
"""
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

# Names retired by glossary section 11. One regex per entry.
REMOVED_NAMES = [
    r"send[- _]?back",            # old review-return term
    r"research brief",            # retired artifact name
    r"\bcoordinator\b",           # retired agent role
    r"confirmation contract",     # retired contract name
    r"research state",            # retired state name
    r"research graph",            # retired graph name
    r"\bHGAR\b",                  # retired architecture name
    r"FE-16",                     # retired requirement ID
    r"writing AIF",               # retired feature name
    r"interaction[_ ]mode",       # retired setting
    r"review[_ ]mode",            # retired setting
    r"\bcopilot\b",               # retired product wording
    r"docker sandbox",            # retired runtime wording
    r"heal ladder",               # retired recovery wording
    r"(?<!release )\bgates?\b",   # retired generic gate (release gate stays)
    r"answer gate",               # retired gate name
]
REMOVED_RE = [re.compile(p, re.I) for p in REMOVED_NAMES]
ALLOW_MARKERS = ("Deprecated", "tên cũ", "Tên đã bỏ")
# Sections that describe history (removed names, mappings, change summaries, stale diagrams) may name
# removed terms. The pattern is anchored to the heading start. Only headings at level 2 or deeper open
# an exempt section, so a mapping file's H1 does not exempt the whole file.
HISTORY_HEADING_RE = re.compile(
    r"^(?:(?i:\d+\.\s*(?:Tên đã bỏ|Diagram))|(?i:Tên đã bỏ|Ánh xạ|Thay đổi so với)|Appendix [A-Z]\b)")

# Code-coupling hints: HTTP codes in prose, REST routes, source paths.
HINTS = [
    (re.compile(r"\b(?:HTTP|status|lỗi|error)\W{0,3}[45]\d\d\b|\b[45]\d\d\W{0,3}(?:HTTP|status|lỗi|error)\b", re.I),
     "HTTP status code in prose"),
    (re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE) /"), "REST route in prose"),
    (re.compile(r"[\w./-]+\.(?:py|tsx?)\b"), "source file path in prose"),
]

# Decision provenance: docs define the system; decision history lives only in changelog.md.
PROVENANCE_RE = [re.compile(p, re.I) for p in (
    r"PM \d{4}-\d{2}-\d{2}",
    r"harness §",
    r"thiết kế (stage )?harness",
    r"owner duyệt",
    r"booklet",
    r"\blogos\b",
)]
PROVENANCE_EXEMPT = {"changelog.md"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slug(text):
    """GitHub-style anchor: lowercase, keep letters/digits/_/-, spaces to '-'."""
    text = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return text.replace(" ", "-")


def anchors(path):
    """Set of heading slugs in a file (duplicates get -1, -2 suffixes)."""
    seen, result, fenced = {}, set(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
        m = None if fenced else HEADING_RE.match(line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0)
            seen[s] = n + 1
            result.add(s if n == 0 else f"{s}-{n}")
    return result


def check_file(path):
    """Return a list of (line, level, message) for one file."""
    out, fenced, history_level = [], False, 0
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        # A history heading opens an allowed section; a heading at the same or a higher level closes it.
        h = None if fenced else HEADING_RE.match(line)
        if h:
            level = len(line) - len(line.lstrip("#"))
            if level >= 2 and HISTORY_HEADING_RE.match(h.group(1)):
                history_level = level
            elif history_level and level <= history_level:
                history_level = 0
        in_removed = bool(history_level)
        if FENCE_RE.match(line):
            fenced = not fenced
            continue

        # Check 1: links resolve to a file and, if given, a heading anchor.
        if not fenced:
            for target in LINK_RE.findall(CODE_SPAN_RE.sub("", line)):
                if re.match(r"(https?:|mailto:)", target):
                    continue
                file_part, _, frag = target.partition("#")
                dest = (path.parent / file_part) if file_part else path
                if not dest.exists():
                    out.append((no, "error", f"broken link: {target}"))
                elif frag and dest.suffix == ".md" and unquote(frag).lower() not in anchors(dest):
                    out.append((no, "error", f"broken anchor: {target}"))

        # Check 2: removed names, unless the line is in a history section or carries an allow marker.
        allowed = in_removed or any(m in line for m in ALLOW_MARKERS)
        if not allowed:
            for rx in REMOVED_RE:
                m = rx.search(line)
                if m:
                    out.append((no, "error", f"removed name '{m.group(0)}'"))

        # Check 3: decision provenance (not in the changelog).
        if path.name not in PROVENANCE_EXEMPT:
            for rx in PROVENANCE_RE:
                m = rx.search(line)
                if m:
                    out.append((no, "error", f"decision provenance '{m.group(0)}'"))

        # Check 4: code-coupling hints (warnings only).
        for rx, msg in HINTS:
            m = rx.search(line)
            if m:
                out.append((no, "warning", f"{msg}: '{m.group(0)}'"))
    return out


def default_files():
    names = ["glossary.md", "README.md", "BRD.md", "PRD.md", "architecture.md", "id-mapping.md", "traceability.md"]
    files = [ROOT / n for n in names]
    files +=sorted((ROOT / "report").glob("*.md")) if (ROOT / "report").is_dir() else []
    return [f for f in files if f.exists()]


def run(files):
    sys.stdout.reconfigure(encoding="utf-8")  # Vietnamese output on cp1252 consoles/pipes
    errors = warnings = 0
    for f in files:
        try:
            shown = f.resolve().relative_to(ROOT)
        except ValueError:
            shown = f
        for no, level, msg in check_file(f):
            print(f"{shown}:{no}: [{level}] {msg}")
            errors += level == "error"
            warnings += level == "warning"
    print(f"{len(files)} file(s), {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def self_test():
    cases = [  # (file content, expected (level, substring) or None for clean)
        ("# A\n[ok](other.md#sec-one)\n", None),
        ("[bad](missing.md)\n", ("error", "broken link")),
        ("[bad](other.md#nope)\n", ("error", "broken anchor")),
        ("Dùng coordinator ở đây.\n", ("error", "removed name")),
        ("| coordinator → orchestrator |\n", ("error", "removed name")),
        ("# Ánh xạ\n\ncoordinator cũ.\n", ("error", "removed name")),
        ("# A\n## Ánh xạ ID\n| coordinator |\n## Khác\nDùng coordinator.\n", ("error", "removed name")),
        ("## Appendix A. Mapping\n| coordinator |\n", None),
        ("## Appendix: ghi chú\nDùng coordinator.\n", ("error", "removed name")),
        ("## 11. Tên đã bỏ\n| coordinator |\n", None),
        ("`[x](missing.md)` trong code.\n", None),
        ("# A\n[ok](#%73ec)\n## Sec\n", None),
        ("Gọi POST /api/x để chạy.\n", ("warning", "REST route")),
        ("Theo quyết định PM 2026-10-29.\n", ("error", "decision provenance")),
        ("Harness là vòng lặp agent; đo bằng harness check.\n", None),
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "other.md").write_text("## Sec one\n", encoding="utf-8")
        for i, (content, expect) in enumerate(cases):
            f = Path(tmp) / f"case{i}.md"
            f.write_text(content, encoding="utf-8")
            got = check_file(f)
            ok = (not got) if expect is None else any(
                lv == expect[0] and expect[1] in msg for _, lv, msg in got)
            print(f"case {i}: {'ok' if ok else 'FAIL'}")
            failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--self-test"]:
        sys.exit(self_test())
    sys.exit(run([Path(a) for a in args] if args else default_files()))
