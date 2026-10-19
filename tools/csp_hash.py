"""Compute SHA-256 CSP hashes for the inline <script> and <style> blocks of a page.

Usage:
  python tools/csp_hash.py v2/index.html          # rewrite the CSP meta in place
  python tools/csp_hash.py v2/index.html --check  # exit 1 if the CSP is out of date (used by CI)

Browsers normalise CRLF to LF before hashing, so the file's line endings don't matter.
"""
import base64
import hashlib
import re
import sys


def digest(block: str) -> str:
    raw = block.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return "'sha256-" + base64.b64encode(hashlib.sha256(raw).digest()).decode() + "'"


def main() -> int:
    path = sys.argv[1]
    check = "--check" in sys.argv[2:]
    with open(path, encoding="utf-8", newline="") as fh:
        html = fh.read()

    scripts = re.findall(r"<script>(.*?)</script>", re.sub(r"<!--.*?-->", "", html, flags=re.S), re.S)
    styles = re.findall(r"<style>(.*?)</style>", re.sub(r"<!--.*?-->", "", html, flags=re.S), re.S)
    if len(scripts) != 1 or len(styles) != 1:
        print(f"expected exactly one inline <script> and one <style>, found {len(scripts)} and {len(styles)}")
        return 1

    want_script, want_style = digest(scripts[0]), digest(styles[0])
    updated = re.sub(r"script-src '[^;\"]*'", "script-src " + want_script, html, count=1)
    updated = re.sub(r"style-src '[^;\"]*'", "style-src " + want_style, updated, count=1)

    if check:
        if updated != html:
            print(f"{path}: CSP hashes are stale. Run: python tools/csp_hash.py {path}")
            return 1
        print(f"{path}: CSP hashes match")
        return 0

    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(updated)
    print(f"{path}: script-src {want_script}  style-src {want_style}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
