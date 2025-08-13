# app.py

from flask import Flask, jsonify, request

app = Flask(__name__)


tea_dict = {
    "green":  "Refreshing tea with a light, grassy flavor",
    "black":  "Strong tea with deep aroma",
    "oolong": "Semi-fermented tea with a floral note",
    "herbal": "Caffeine-free tea from herbs",
}

ENABLE_AUTH = True          
EXPECTED_TOKEN = "secret123"

@app.before_request
def simple_auth():
    if not ENABLE_AUTH:
        return
   
    if request.method == "GET" and request.path.startswith("/tea"):
        return
   
    auth = request.headers.get("Authorization", "")
    ok = auth.startswith("Bearer ") and auth.split(" ", 1)[1] == EXPECTED_TOKEN
    if not ok:
        resp = jsonify(error="Unauthorized")
        resp.status_code = 401
        resp.headers["WWW-Authenticate"] = "Bearer"
        return resp


@app.after_request
def add_api_version(resp):
    resp.headers["X-API-Version"] = "2"
    return resp


@app.route("/tea", methods=["GET"])
def list_or_search_tea():
    q = request.args.get("q", type=str)

   
    all_teas = [{"name": n, "description": d} for n, d in tea_dict.items()]

    if q is None or q.strip() == "":
        return jsonify(all_teas), 200

    ql = q.lower().strip()
    results = [
        it for it in all_teas
        if (ql in it["name"]) or (ql in it["description"].lower())
    ]
    return jsonify(results), 200


@app.route("/tea/<name>", methods=["GET"])
def get_tea(name):
    key = name.lower().strip()
    description = tea_dict.get(key)
    if description is None:
        return jsonify(error="The tea not found"), 404
    return jsonify(name=key, description=description), 200


@app.route("/tea", methods=["POST"])
def add_tea():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Invalid or missing JSON body"), 400

    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    if not name or not description:
        return jsonify(error="Please provide both 'name' and 'description'"), 400

    key = name.lower()
    if key in tea_dict:
        return jsonify(error=f"Tea '{key}' already exists"), 409

    if len(description) > 200:
        return jsonify(error="Description is too long (max 200 chars)"), 422

    tea_dict[key] = description
    return jsonify(message="Tea created", name=key, description=description), 201


@app.route("/tea/<name>", methods=["PUT", "PATCH"])
def update_tea(name):
    key = name.lower().strip()
    if key not in tea_dict:
        return jsonify(error="Tea not found"), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Invalid or missing JSON body"), 400

    description = (data.get("description") or "").strip()
    if not description:
        return jsonify(error="Please provide non-empty 'description'"), 400

    if len(description) > 200:
        return jsonify(error="Description is too long (max 200 chars)"), 422

    tea_dict[key] = description
    return jsonify(message="Tea updated", name=key, description=description), 200


@app.route("/tea/<name>", methods=["DELETE"])
def delete_tea(name):
    key = name.lower().strip()
    if key not in tea_dict:
        return jsonify(error="Tea not found"), 404
    del tea_dict[key]
    return ("", 204)


if __name__ == "__main__":

  🧪 Example Requests (cURL)
List and Search
curl http://127.0.0.1:5000/tea
curl "http://127.0.0.1:5000/tea?q=floral"
Get One
bash
Copier
Modifier
curl -i http://127.0.0.1:5000/tea/green
curl -i http://127.0.0.1:5000/tea/jasmine   # 404
Create (POST)
bash
Copier
Modifier
curl -i -X POST http://127.0.0.1:5000/tea \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret123" \
  -d '{"name":"white","description":"Delicate tea with floral aroma"}'

Update (PATCH / PUT)
bash
Copier
Modifier
curl -i -X PATCH http://127.0.0.1:5000/tea/white \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret123" \
  -d '{"description":"Gentle white tea with sweet notes"}'

curl -i -X PUT http://127.0.0.1:5000/tea/white \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret123" \
  -d '{"description":"Very strong white tea"}'
Delete
bash
Copier
Modifier
curl -i -X DELETE http://127.0.0.1:5000/tea/white \
  -H "Authorization: Bearer secret123"


  
