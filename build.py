#!/usr/bin/env python3
"""Wrap schedule.html (the Artifact page body) into a standalone index.html.

schedule.html is written for the Claude Artifact viewer, which supplies the
document skeleton (doctype, charset, viewport, a small reset). A plain web
server supplies none of that, so this script adds it and splits the head
tags from the body content.

    python3 build.py
"""
import io, sys, pathlib

SRC = pathlib.Path(__file__).parent / "schedule.html"
OUT = pathlib.Path(__file__).parent / "index.html"
SPLIT = '<div class="wrap">'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="A hand-drawn 24-hour dial on Winnipeg time that shows the activity you are in right now.">
<meta name="theme-color" content="#FBF1DB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131A40" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="My schedule">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<style>
:root{
  color-scheme:light;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""

FOOT = """</body>
</html>
"""

def main():
    src = io.open(SRC, encoding="utf-8").read()
    if SPLIT not in src:
        sys.exit("build: could not find %r in %s" % (SPLIT, SRC.name))
    head_part, body_part = src.split(SPLIT, 1)
    doc = HEAD + head_part.rstrip() + "\n</head>\n<body>\n" + SPLIT + body_part.rstrip() + "\n" + FOOT
    io.open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote %s (%d bytes)" % (OUT.name, len(doc.encode("utf-8"))))

if __name__ == "__main__":
    main()
