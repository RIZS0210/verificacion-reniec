from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)


reniec_db = {
    "72926391": {
        "nombres": "RECHAEL DARIO",
        "apellidos": "ZAVALETA SANTISTEBAN",
        "foto": "https://raw.githubusercontent.com/RIZS0210/verificacion-reniec/b6d687dc30d35dbbedea9e6c2a793e4b80287016/fotos/Imagen%20de%20WhatsApp%202025-09-11%20a%20las%2021.13.31_e2155269.jpg"
    },
    "72759900": {  # <- NUEVO REGISTRO
        "nombres": "GRECIA HACIEL",
        "apellidos": "PLASENCIA ALVA",
        "foto": "https://raw.githubusercontent.com/RIZS0210/verificacion-reniec/main/fotos/haciel.jpg"  # <- cambia a tu URL real
    }
}


# Función para convertir imagen desde URL a Base64
def imagen_a_base64(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        imagen_bytes = BytesIO(response.content)
        encoded = base64.b64encode(imagen_bytes.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        print("Error al convertir la imagen a base64:", e)
        return None

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
            # Convertir la foto a Base64
            foto_base64 = imagen_a_base64(persona["foto"])
            if not foto_base64:
                return jsonify({"status": "error", "mensaje": "❌ No se pudo procesar la foto"})
            
            # Devolver los datos con la foto en base64
            return jsonify({
                "status": "ok",
                "mensaje": "✅ Identidad verificada",
                "datos": {
                    "nombres": persona["nombres"],
                    "apellidos": persona["apellidos"],
                    "foto_base64": foto_base64
                }
            })
        else:
            return jsonify({"status": "error", "mensaje": "❌ Los datos no coinciden"})
    else:
        return jsonify({"status": "error", "mensaje": "❌ DNI no encontrado en la base"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



