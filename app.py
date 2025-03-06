from flask import Flask, request, jsonify
import os
from jinja2 import Environment, FileSystemLoader
from src.ImageProcessing import analyze_plant_health  

# Initialisation de Flask
app = Flask(__name__)

# Définition du dossier contenant les templates HTML
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint Flask pour analyser une image Base64 et retourner un HTML.
    """
    try:
        # Récupérer les données JSON de la requête
        data = request.get_json()
        if not data or "image_base64" not in data:
            return jsonify({"error": "Requête invalide", "details": "L'image Base64 est requise"}), 400

        image_base64 = data["image_base64"]

        # Vérifier que le format Base64 est correct
        index_base64 = image_base64.find("base64,")
        if index_base64 == -1:
            return jsonify({"error": "Format incorrect", "details": "Base64 mal formé"}), 400

        # Extraire uniquement la partie encodée
        image_base64.strip('"')
        image_base64 = image_base64[index_base64 + len("base64,"):]

        # Analyser l'image avec OpenAI
        response, status_code = analyze_plant_health(image_base64)

        # Vérifier si OpenAI a retourné une erreur
        if "error" in response:
            return jsonify(response), status_code

        # Générer le bon template en fonction de la réponse
        if response["isPlant"] == 0:
            template = env.get_template("error_not_plant.html")
            html_result = template.render()
        elif response["status"] == "good health":
            template = env.get_template("healthy_plant.html")
            html_result = template.render(diag=response["diag"])
        else:
            template = env.get_template("sick_plant.html")
            badge_color = "sick" if response["status"] == "sick" else "very-sick"
            html_result = template.render(
                badgeColor=badge_color,
                status=response["status"],
                diag=response["diag"],
                solution=response["solution"]
            )

        # Retourner la réponse JSON avec le HTML généré
        return jsonify({
            "HtmlResult": html_result,
            "isPlant": response["isPlant"]
        }), 200

    except Exception as e:
        return jsonify({"error": "Erreur interne", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
