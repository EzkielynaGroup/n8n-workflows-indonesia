#!/usr/bin/env python3
"""Cek cepat semua workflow di folder workflows/ sebelum commit.

Memeriksa: JSON valid, ada key "nodes" dan "connections", setiap node punya
id/name/type/typeVersion/position/parameters, nama node unik, koneksi menunjuk ke
node yang ada, dan credential hanya berisi nama (tanpa id atau data rahasia).

Pakai: python3 scripts/validate.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "workflows"
SECRET = re.compile(r"sk-[A-Za-z0-9_-]{16,}|Bearer\s+[A-Za-z0-9._-]{16,}")
errors = []

for path in sorted(ROOT.glob("*.json")):
    raw = path.read_text(encoding="utf-8")
    try:
        wf = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"{path.name}: JSON tidak valid ({e})")
        continue
    for key in ("name", "nodes", "connections"):
        if key not in wf:
            errors.append(f"{path.name}: tidak ada key '{key}'")
    names = set()
    for n in wf.get("nodes", []):
        for key in ("id", "name", "type", "typeVersion", "position", "parameters"):
            if key not in n:
                errors.append(f"{path.name}: node {n.get('name')!r} tidak punya '{key}'")
        if n.get("name") in names:
            errors.append(f"{path.name}: nama node dobel {n.get('name')!r}")
        names.add(n.get("name"))
        for cred_type, cred in (n.get("credentials") or {}).items():
            if set(cred) - {"name"}:
                errors.append(f"{path.name}: credential {cred_type} di {n['name']!r} sebaiknya hanya berisi 'name'")
    for src, outputs in wf.get("connections", {}).items():
        if src not in names:
            errors.append(f"{path.name}: koneksi dari node yang tidak ada {src!r}")
        for branches in outputs.values():
            for branch in branches:
                for link in branch:
                    if link.get("node") not in names:
                        errors.append(f"{path.name}: koneksi ke node yang tidak ada {link.get('node')!r}")
    if SECRET.search(raw):
        errors.append(f"{path.name}: ada teks yang mirip API key asli")
    print(f"ok  {path.name}: {len(wf.get('nodes', []))} node")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Semua workflow valid.")
