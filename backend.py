from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # UTF-8 zorla

ANA_API = "http://45.81.113.22:5000"

# ------------------ Güvenli Temizleme ------------------

def temizle(v):
    if not v:
        return ""
    return re.sub(r"[^\x20-\x7E]", "", str(v))

def proxy_yolla(endpoint, params):
    try:
        r = requests.get(f"{ANA_API}{endpoint}", params=params, timeout=10)
        r.encoding = "utf-8"
        return jsonify(r.json())
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Ana API ulaşılamıyor",
            "detail": str(e)
        })

# ------------------ ROUTES ------------------

@app.route("/key/olustur")
def key_olustur():
    tip = temizle(request.args.get("tip"))
    return proxy_yolla("/key/olustur", {"tip": tip})

@app.route("/key/kontrol")
def key_kontrol():
    key = temizle(request.args.get("key"))
    return proxy_yolla("/key/kontrol", {"key": key})

@app.route("/key/sil")
def key_sil():
    key = temizle(request.args.get("key"))
    return proxy_yolla("/key/sil", {"key": key})

# ------------------ Render ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
