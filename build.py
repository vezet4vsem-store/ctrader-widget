#!/usr/bin/env python3
"""Inline products.json into index.html (fallback data) and produce standalone.html.

Usage:  python3 build.py
- index.html      : keeps fetching products.json at runtime; inline copy is a fallback
- standalone.html : single file with everything inside — for preview, email, or hosting where
                    products.json can't be served (no build step needed to edit products.json otherwise)
"""
import json, re, pathlib

root = pathlib.Path(__file__).parent
data = json.loads((root / "products.json").read_text(encoding="utf-8"))
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

src = (root / "index.html").read_text(encoding="utf-8")
pat = re.compile(r'(<script id="products-data" type="application/json">)(.*?)(</script>)', re.S)
out = pat.sub(lambda m: m.group(1) + compact + m.group(3), src, count=1)
(root / "index.html").write_text(out, encoding="utf-8")

# standalone: skip the fetch entirely
standalone = out.replace("const r = await fetch('products.json', { cache: 'no-cache' });", "throw new Error('standalone');")
(root / "standalone.html").write_text(standalone, encoding="utf-8")
print(f"ok: {len(data['products'])} products inlined")
