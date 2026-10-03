"""Fail if any deliverable contains an em dash, en dash, or emoji."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.schema import BANNED_RE  # noqa: E402

# Raw archived or fetched source files (including agent scratch copies) are preserved byte for byte and are not deliverables.
RAW_DIRS = ("phase1/targeted/wayback/", "phase1/targeted/archives/", "phase1/targeted/pdfs/", "phase1/targeted/sweep/", "phase1/targeted/sweep2/", "phase1/wayback_snapshots/", "phase1/scratch/")
TEXT_EXT = {".md", ".csv", ".py", ".js", ".html", ".toml", ".json", ".txt", ".ps1", ".bat", ".cmd", ".yml", ".yaml"}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=root,
                           capture_output=True, text=True, check=True).stdout.split("\n")
    bad = []
    for f in filter(None, files):
        if f.startswith(RAW_DIRS):
            continue
        p = root / f
        if p.suffix.lower() in TEXT_EXT and p.exists():
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if BANNED_RE.search(line):
                    bad.append(f"{f}:{i}: {line.strip()[:120]}")
        if p.suffix.lower() == ".docx" and p.exists():
            import docx
            text = "\n".join(par.text for par in docx.Document(str(p)).paragraphs)
            if BANNED_RE.search(text):
                bad.append(f"{f}: banned character in document text")
    print("\n".join(bad) if bad else "style check clean")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
