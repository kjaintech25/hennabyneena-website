#!/usr/bin/env python3
"""Point the site's absolute URLs at a new domain.

    python3 tools/set-domain.py https://hennabyneenajain.com

Rewrites every hardcoded base URL across the four HTML pages, sitemap.xml and
robots.txt. Those absolute URLs live in:
  - <link rel="canonical">
  - og:url, og:image, twitter:image
  - the LocalBusiness JSON-LD (@id, url, image, logo)
  - sitemap <loc> entries and the robots.txt Sitemap line

Run it only once the domain actually resolves — a canonical tag pointing at a
dead host tells Google to drop the page.

Pass --check to see what would change without writing anything.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

FILES = ["index.html", "gallery.html", "faq.html", "book.html",
         "sitemap.xml", "robots.txt"]

# Matches any scheme://host(/path) we've previously used as the base.
KNOWN_BASES = [
    "https://kjaintech25.github.io/hennabyneena-website",
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if len(args) != 1:
        sys.exit("usage: set-domain.py https://example.com [--check]")

    new = args[0].rstrip("/")
    if not re.match(r"^https?://[^/]+$", new):
        sys.exit(f"expected a bare origin like https://example.com, got: {new}")

    total = 0
    for name in FILES:
        path = os.path.join(SITE, name)
        if not os.path.exists(path):
            print(f"  skip {name} (missing)")
            continue
        s = open(path, encoding="utf-8").read()
        before = s
        for old in KNOWN_BASES:
            s = s.replace(old, new)
        n = sum(before.count(old) for old in KNOWN_BASES)
        if n:
            total += n
            if not check:
                open(path, "w", encoding="utf-8").write(s)
        print(f"  {name:14} {n} replaced")

    print(f"\n{'would replace' if check else 'replaced'} {total} URLs -> {new}")
    if total and not check:
        print("\nNow update KNOWN_BASES in this script to include the new base,\n"
              "so a future domain change can find it.")


if __name__ == "__main__":
    main()
