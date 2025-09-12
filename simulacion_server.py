from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Importar CORS

app = Flask(__name__)
CORS(app)  # 👈 Habilitar CORS en toda la app

# Simulación de base de datos
reniec_db = {
    "72926391": {"nombres": "RECHAEL DARIO", "apellidos": "ZAVALETA SANTISTEBAN"},
    "87654321": {"nombres": "MARIA", "apellidos": "LOPEZ RAMOS"}
}

# Ruta raíz para probar que el servidor funciona
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "mensaje": "Servidor funcionando 🚀"})

# Ruta para verificación de identidad
@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.json
    dni = data.get("dni")
    nombres = data.get("nombres", "").upper()
    apellidos = data.get("apellidos", "").upper()

    if dni in reniec_db:
        persona = reniec_db[dni]
        if persona["nombres"] == nombres and persona["apellidos"] == apellidos:
            return jsonify({"status": "ok", "mensaje": "✅ Identidad verificada"})
        else:
            return jsonify({"status": "error", "mensaje": "❌ Los datos no coinciden"})
    else:
        return jsonify({"status": "error", "mensaje": "❌ DNI no encontrado en la base"})

if __name__ == "__main__":
    # Render espera que corras en el puerto 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
