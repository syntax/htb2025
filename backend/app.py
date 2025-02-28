from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the HTB2025 API",
        "status": "success"
    }), 200

@app.route('/echo', methods=['POST'])
def echo():
    if not request.json:
        abort(400, "Request must be in JSON format.")
    return jsonify({
        "you_sent": request.json
    }), 200

items = []

@app.route('/api/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return jsonify({"items": items}), 200

    if request.method == 'POST':
        if not request.json or 'name' not in request.json:
            abort(400, "Missing 'name' in JSON body.")
        item = {
            "id": len(items) + 1,
            "name": request.json['name']
        }
        items.append(item)
        return jsonify({"item": item}), 201

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        abort(404, f"Item with id {item_id} not found.")

    if request.method == 'GET':
        return jsonify({"item": item}), 200

    if request.method == 'PUT':
        if not request.json or 'name' not in request.json:
            abort(400, "Missing 'name' in JSON body.")
        item['name'] = request.json['name']
        return jsonify({"item": item}), 200

    if request.method == 'DELETE':
        items.remove(item)
        return jsonify({"result": True}), 200
