"""Generate docs/API.md from the FastAPI OpenAPI schema.

Usage: python scripts/generate_api_docs.py
Writes a compact endpoint reference — accurate by construction, no drift.
"""

import pathlib
import sys

# Scripts live in scripts/ — make the repo root importable (sys.path[0] is scripts/)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from api.main import app

METHODS = ("get", "post", "put", "delete", "patch")

spec = app.openapi()
paths = spec["paths"]

lines = [
    "# SIH26184 — API Reference (v1)",
    "",
    f"Generated from the FastAPI OpenAPI schema · **{len(paths)} paths** · "
    "interactive UI at `/docs` (Swagger) and `/redoc`.",
    "",
    "Auth: `Authorization: Bearer <access_token>` per role "
    "(ADMIN / INSPECTOR / CONSTABLE) — see `POST /api/v1/auth/login`.",
    "",
]

for path in sorted(paths):
    for method, op in sorted(paths[path].items()):
        if method not in METHODS:
            continue
        summary = (op.get("summary") or "").strip()
        tags = ", ".join(op.get("tags", []))
        lines.append(f"## {method.upper()} `{path}`")
        if summary:
            lines.append(f"**{summary}**  [{tags}]")
        lines.append("")

out = "\n".join(lines)
out_path = pathlib.Path("docs") / "API.md"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(out, encoding="utf-8")
print(f"Wrote {out_path}: {len(paths)} paths, {len(out)} chars")
