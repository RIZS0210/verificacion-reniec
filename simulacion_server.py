from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de datos simulada con foto (URL pública de tu GitHub Pages)
reniec_db = {
    "72926391": {
        "nombres": "RECHAEL DARIO",
        "apellidos": "ZAVALETA SANTISTEBAN",
        "foto": "https://tuusuario.github.io/tu-repo/fotos/Imagen de WhatsApp 2025-09-11 a las 21.13.31_e2155269.jpg"
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "mensaje": "Servidor funcionando 🚀"})

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.json
    dni = data.get("dni")
    nombres = data.get("nombres", "").upper()
    apellidos = data.get("apellidos", "").upper()

    if dni in reniec_db:
        persona = reniec_db[dni]
        if persona["nombres"] == nombres and persona["apellidos"] == apellidos:
            # Devuelve también la foto
            return jsonify({
                "status": "ok",
                "mensaje": "✅ Identidad verificada",
                "datos": persona
            })
        else:
            return jsonify({"status": "error", "mensaje": "❌ Los datos no coinciden"})
    else:
        return jsonify({"status": "error", "mensaje": "❌ DNI no encontrado en la base"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
