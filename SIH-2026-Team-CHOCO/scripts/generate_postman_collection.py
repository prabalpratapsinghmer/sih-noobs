#!/usr/bin/env python3
"""Generate Postman 2.1 collection from the app's OpenAPI spec.

Run: python scripts/generate_postman_collection.py
Output: docs/postman_collection.json

Driven entirely from ``app.openapi()`` (public API) instead of FastAPI route
internals, so it survives framework upgrades. Auth endpoints are added
manually in an "Authentication" folder (login JSON + OAuth2 form token).
"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from api.main import app  # noqa: E402 — build the app, then read its OpenAPI spec

BASE_URL = "http://localhost:8000"
API_VERSION = "v1"

_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")


def _resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a JSON-Schema ``$ref`` (``#/components/schemas/X``) in the spec."""
    node = spec
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def _sample_from_schema(schema: dict, spec: dict) -> object:
    """Synthesize a JSON example value from a JSON-Schema (with $ref resolution).

    Preference: explicit ``example`` → ``default`` → ``enum`` first value →
    type-based placeholder. Only required object properties are included so
    sample bodies stay minimal and valid.
    """
    if "$ref" in schema:
        schema = _resolve_ref(spec, schema["$ref"])
    if "example" in schema:
        return schema["example"]
    if "default" in schema and schema["default"] is not None:
        return schema["default"]
    if "enum" in schema:
        return schema["enum"][0]

    schema_type = schema.get("type")
    if schema_type == "object" or "properties" in schema:
        required = set(schema.get("required") or [])
        result = {}
        for name, prop in (schema.get("properties") or {}).items():
            prop_has_default = "default" in prop and prop["default"] is not None
            if name in required or "example" in prop or prop_has_default:
                result[name] = _sample_from_schema(prop, spec)
        return result
    if schema_type == "array":
        return [_sample_from_schema(schema.get("items") or {}, spec)]
    if schema_type in ("integer", "number"):
        return 0
    if schema_type == "boolean":
        return False
    return "string"


def _item_body(spec: dict, op: dict):
    """Build a Postman request body from the operation's requestBody."""
    request_body = op.get("requestBody") or {}
    content = (request_body.get("content") or {}).get("application/json")
    if content:
        example = _sample_from_schema(content.get("schema") or {}, spec)
        if example:
            return {
                "mode": "raw",
                "raw": json.dumps(example, indent=2),
                "options": {"raw": {"language": "json"}},
            }
    return None


def item_from_operation(spec: dict, path: str, verb: str, op: dict) -> dict:
    """Convert one OpenAPI operation to a Postman 2.1 item."""
    path_params = [p for p in op.get("parameters", []) if p.get("in") == "path"]
    query_params = [p for p in op.get("parameters", []) if p.get("in") == "query"]

    name = op.get("summary") or f"{verb} {path}"
    desc = op.get("description") or ""

    request = {
        "method": verb,
        "header": [],
        "url": {
            "raw": f"{BASE_URL}{path}",
            "host": [BASE_URL.replace("http://", "").replace("https://", "")],
            "path": [p.strip("/") for p in path.strip("/").split("/")],
            "query": [
                {"key": q["name"], "value": "", "description": q.get("description", "")}
                for q in query_params
            ],
        },
        "description": desc,
    }

    if path_params:
        request["url"]["variable"] = [
            {
                "key": p["name"],
                "value": p["name"],
                "description": p.get("description", ""),
                "type": "text",
            }
            for p in path_params
        ]

    if verb in ("POST", "PUT", "PATCH"):
        body = _item_body(spec, op)
        if body:
            request["body"] = body

    return {"name": name, "request": request, "response": []}


def auth_info():
    """Generate auth template for the collection."""
    return {
        "type": "bearer",
        "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}],
    }


def main():
    spec = app.openapi()
    api_prefix = f"/api/{API_VERSION}/"

    routes = []
    for path, ops in sorted(spec.get("paths", {}).items()):
        if not path.startswith(api_prefix):
            continue
        for method in _METHODS:
            op = ops.get(method.lower())
            if op is None:
                continue
            # Form endpoint is documented manually in the Authentication folder
            if path == f"{api_prefix}auth/token" and method == "POST":
                continue
            routes.append((path, method, op))

    items = []
    current_prefix = None
    for path, method, op in routes:
        prefix = path[len(api_prefix):].split("/")[0]  # /api/v1/{prefix}/...
        if prefix != current_prefix:
            current_prefix = prefix
            items.append({"name": prefix.upper(), "item": []})
        items[-1]["item"].append(item_from_operation(spec, path, method, op))

    collection = {
        "info": {
            "name": f"SIH26184 API ({API_VERSION})",
            "description": (
                "Predictive Analytics Framework for Cybercrime Complaints\n\n"
                f"Generated: {datetime.now(UTC).isoformat()}\n"
                f"Base URL: {BASE_URL}\n\n"
                "**Demo credentials:**\n"
                "- admin/admin123\n"
                "- inspector1/inspector123\n"
                "- constable1/constable123"
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "variable": [
            {"key": "baseUrl", "value": BASE_URL, "type": "string"},
            {"key": "access_token", "value": "", "type": "string"},
            {"key": "refresh_token", "value": "", "type": "string"},
        ],
        "auth": auth_info(),
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "Login (JSON)",
                        "request": {
                            "method": "POST",
                            "header": [{"key": "Content-Type", "value": "application/json"}],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({"username": "admin", "password": "admin123"}, indent=2),
                                "options": {"raw": {"language": "json"}},
                            },
                            "url": {
                                "raw": f"{BASE_URL}/api/{API_VERSION}/auth/login",
                                "host": [BASE_URL.replace("http://", "")],
                                "path": [API_VERSION, "auth", "login"],
                            },
                        },
                    },
                    {
                        "name": "OAuth2 Token (form)",
                        "request": {
                            "method": "POST",
                            "header": [{"key": "Content-Type", "value": "application/x-www-form-urlencoded"}],
                            "body": {
                                "mode": "urlencoded",
                                "urlencoded": [
                                    {"key": "username", "value": "admin"},
                                    {"key": "password", "value": "admin123"},
                                    {"key": "grant_type", "value": "password"},
                                ],
                            },
                            "url": {
                                "raw": f"{BASE_URL}/api/{API_VERSION}/auth/token",
                                "host": [BASE_URL.replace("http://", "")],
                                "path": [API_VERSION, "auth", "token"],
                            },
                        },
                    },
                    {
                        "name": "Refresh Token",
                        "request": {
                            "method": "POST",
                            "header": [{"key": "Content-Type", "value": "application/json"}],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({"refresh_token": "{{refresh_token}}"}, indent=2),
                                "options": {"raw": {"language": "json"}},
                            },
                            "url": {
                                "raw": f"{BASE_URL}/api/{API_VERSION}/auth/refresh",
                                "host": [BASE_URL.replace("http://", "")],
                                "path": [API_VERSION, "auth", "refresh"],
                            },
                        },
                    },
                    {
                        "name": "Logout",
                        "request": {
                            "method": "POST",
                            "url": {
                                "raw": f"{BASE_URL}/api/{API_VERSION}/auth/logout",
                                "host": [BASE_URL.replace("http://", "")],
                                "path": [API_VERSION, "auth", "logout"],
                            },
                        },
                    },
                ],
            },
            *items,
        ],
    }

    out_path = Path(__file__).parent.parent / "docs" / "postman_collection.json"
    out_path.write_text(json.dumps(collection, indent=2))
    print(f"Generated Postman collection: {out_path}")
    print(f"Operations documented: {len(routes)}")


if __name__ == "__main__":
    main()
