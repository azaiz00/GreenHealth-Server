from flask import Flask, request, jsonify
from jinja2 import Environment, FileSystemLoader
from src.ImageProcessing import analyze_plant_health  
from flask import Flask, render_template
import os
import re



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
           
        elif response["status"] == "Bonne santé":
            template = env.get_template("healthy_plant.html")
            html_result = template.render(
                status=response["status"],
                diag=response["diag"],
                Recommandations=response["solution"])
        else:
            template = env.get_template("sick_plant.html")
            badge_color = "Malade" if response["status"] == "Malade" else "Très malade"
            html_result = template.render(
                badgeColor=badge_color,
                status=response["status"],
                diag=response["diag"],
                solution=response["solution"]
            )

        # Nettoyer le HTML pour PowerApps

            # Remplace les guillemets " par des apostrophes '
        html_result = html_result.replace('"', "'")
        
            # Supprime les retours à la ligne et les backslashes
        html_result = re.sub(r'\\n', '', html_result)  # Supprime \n
        html_result = re.sub(r'\\', '', html_result)   # Supprime \ 

        # Retourner la réponse JSON avec le HTML nettoyé
        return jsonify({
            "HtmlResult": html_result,
            "isPlant": str(response["isPlant"])
        }), 200

    except Exception as e:
        return jsonify({"error": "Erreur interne", "details": str(e)}), 500



@app.route('/render', methods=['POST'])  # Changement d'URL pour plus de clarté
def render_template_from_request():
    """ Rend une template HTML en fonction de la requête POST """
    data = request.json  # Récupération des données envoyées en JSON
    template_name = data.get("template", "error_not_plant.html")  # Valeur par défaut
    context = data.get("context", {})  # Dictionnaire contenant des variables pour la template

    try:
        return render_template(template_name, **context)
    except:
        return "Template not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
