# app_work.py
from flask import Flask, request, jsonify
from ws_crud_work import (
    create_work, get_work, list_works, update_work, patch_work, delete_work
)

app = Flask(__name__)

@app.get("/")
def health():
    return {"service": "works", "status": "ok"}

# --------- CREATE ---------
@app.post("/works")
def api_create_work():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    theme = data.get("theme")
    if not title:
        return jsonify({"error": "El campo 'title' es obligatorio"}), 400
    try:
        row = create_work(title, theme)
        return jsonify(row), 201
    except Exception as e:
        return jsonify({"error": f"Error interno: {e}"}), 500

# --------- READ ALL ---------
@app.get("/works")
def api_list_works():
    q = request.args.get("q")
    theme = request.args.get("theme")
    order = request.args.get("order", "desc")
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit/offset deben ser enteros"}), 400

    limit = max(1, min(100, limit))
    offset = max(0, offset)
    try:
        payload = list_works(q=q, theme=theme, limit=limit, offset=offset, order=order)
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": f"Error interno: {e}"}), 500

# --------- READ ONE ---------
@app.get("/works/<int:work_id>")
def api_get_work(work_id: int):
    row = get_work(work_id)
    if not row:
        return jsonify({"message": f"Work con ID {work_id} no encontrado"}), 404
    return jsonify(row), 200

# --------- UPDATE (PUT) ---------
@app.put("/works/<int:work_id>")
def api_update_work(work_id: int):
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    theme = data.get("theme")
    if not title:
        return jsonify({"error": "El campo 'title' es obligatorio"}), 400

    row = update_work(work_id, title, theme)
    if not row:
        return jsonify({"message": f"Work con ID {work_id} no encontrado"}), 404
    return jsonify(row), 200

# --------- PATCH (partial) ---------
@app.patch("/works/<int:work_id>")
def api_patch_work(work_id: int):
    data = request.get_json(silent=True) or {}
    try:
        row = patch_work(work_id, data)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    if not row:
        return jsonify({"message": f"Work con ID {work_id} no encontrado"}), 404
    return jsonify(row), 200

# --------- DELETE ---------
@app.delete("/works/<int:work_id>")
def api_delete_work(work_id: int):
    ok = delete_work(work_id)
    if not ok:
        return jsonify({"message": f"Work con ID {work_id} no encontrado para eliminar"}), 404
    return jsonify({"message": f"Work con ID {work_id} eliminado con éxito"}), 200

if __name__ == "__main__":
    # corre en 8001, para no chocar con app_edition.py (8000)
    app.run(host="0.0.0.0", port=8001, debug=True)
