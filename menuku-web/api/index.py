"""Endpoint API MenuKu untuk Vercel.

Bisa dijalankan langsung secara lokal:

    python api/index.py

Pada Vercel, file ini dipakai sebagai Python serverless function.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIR = os.path.join(BASE_DIR, "..", "python")
PUBLIC_DIR = os.path.join(BASE_DIR, "..", "public")

sys.path.insert(0, os.path.abspath(PYTHON_DIR))

from recipe_data import RECIPES, required_ingredients
from template_recommendation import recommend_with_fallback


def _serialize(result):
    recommendations = []

    for rec in result:
        recommendations.append({
            "id": rec.recipe["id"],
            "name": rec.recipe["name"],
            "matched": len(rec.matched_ingredients),
            "required": len(required_ingredients(rec.recipe)),
            "matched_ingredients": rec.matched_ingredients,
            "missing_ingredients": rec.missing_ingredients,
            "matched_optional": rec.matched_optional,
            "steps": rec.recipe["steps"],
        })

    return {
        "source": getattr(result, "source", ""),
        "only_risky": result.only_risky,
        "warnings": list(result.warnings),
        "message": result.message,
        "recommendations": recommendations,
    }


def _json_response(handler, status, body):
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


class handler(BaseHTTPRequestHandler):
    def _serve_static(self, path):
        path = path.lstrip("/") or "index.html"
        full_path = os.path.join(PUBLIC_DIR, path)

        if not os.path.isfile(full_path):
            self.send_error(404)
            return

        with open(full_path, "rb") as file:
            content = file.read()

        content_type = "text/plain"
        if full_path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif full_path.endswith(".css"):
            content_type = "text/css"
        elif full_path.endswith(".js"):
            content_type = "application/javascript"
        elif full_path.endswith(".json") or full_path.endswith(".webmanifest"):
            content_type = "application/json"
        elif full_path.endswith(".png"):
            content_type = "image/png"
        elif full_path.endswith(".svg"):
            content_type = "image/svg+xml"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path.startswith("/api/health"):
            _json_response(self, 200, {"status": "ok"})
        else:
            self._serve_static(self.path)

    def do_POST(self):
        if not self.path.startswith("/api/recommend"):
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            ingredients = data.get("ingredients", [])
        except Exception:
            _json_response(self, 400, {"error": "invalid_json"})
            return

        if not isinstance(ingredients, list):
            _json_response(self, 400, {"error": "ingredients_must_be_list"})
            return

        result = recommend_with_fallback(ingredients)
        _json_response(self, 200, _serialize(result))


if __name__ == "__main__":
    from http.server import HTTPServer

    port = int(os.environ.get("PORT", 8000))
    print(f"MenuKu web berjalan di http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), handler).serve_forever()
