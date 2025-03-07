import openai
import json
import os
import re
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser OpenAI avec la clé API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("ERREUR : La clé API OpenAI est absente ou incorrecte")

# Initialiser le client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Utilisation du modèle GPT-4o-mini (ou un autre modèle si besoin)
model = "gpt-4o-mini"

def analyze_plant_health(image_base64):
    print("test")
    """
    Analyse une image de plante avec GPT-4o et retourne un diagnostic structuré.
    """
    try:
        # Envoyer la requête à OpenAI pour obtenir le diagnostic
        response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Vous êtes un expert en botanique."
                    "\n"
                    "Critères d'analyse :\n"
                    "- Si l'image ne représente pas une plante : 'status' = '', 'diag' = 'Cette image ne contient pas une plante.','solution' = '', 'isPlant' = 0\n"
                    "- Si la plante est en bonne santé : 'status' = 'Bonne santé', 'diag' = 'Explication de son bon état', 'solution' = 'Conseils d’entretien pour garder ou améliorer la qualité ', 'isPlant' = 1\n"
                    "- Si la plante est malade : 'status' = 'Malade' ou 'Très malade', 'diag' = 'Explication très détaillée de l’état de la plante avec symptômes observés et causes possibles', 'solution' = 'Explication détaillée des actions à prendre pour chaque cause potentielle','isPlant' = 1\n"
                    "Fournissez UNIQUEMENT un JSON structuré sous ce format : "
                    "{ 'status': 'Bonne santé' | 'Malade' | 'Très malade' | '', "
                    "'diag': 'Explication détaillée...', "
                    "'solution': 'Solution détaillée...', "
                    "'isPlant': 1 ou 0 }. "
                    "Aucun texte supplémentaire n'est autorisé."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Voici une photo d'une plante. Fournissez un diagnostic structuré au format JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ],
            },
        ],
        temperature=0.3,
        max_tokens=1500  # Ajusté pour permettre un diagnostic et une solution détaillés
    )

        # Vérifier si la réponse OpenAI contient des choix
        if not response.choices:
            return {"error": "Erreur API OpenAI", "details": "Réponse vide d'OpenAI"}, 500

        # Initialiser json_match à None pour éviter les erreurs si la regex échoue
        json_match = None  

        # Récupérer la réponse textuelle de OpenAI
        response_text = response.choices[0].message.content.strip()

        # Rechercher uniquement la partie JSON dans la réponse OpenAI
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if json_match:
            try:
                plant_data = json.loads(json_match.group(0))  # Convertir uniquement le JSON extrait
            except json.JSONDecodeError as e:
                return {"error": "Erreur de parsing de la réponse OpenAI", "details": str(e)}, 500
        else:
            return {"error": "Réponse OpenAI invalide", "details": "Aucun JSON détecté"}, 500


        # Vérification des valeurs renvoyées
        if "isPlant" not in plant_data:
            return {"error": "Données manquantes", "details": "Champ 'isPlant' absent du JSON"}, 500

        # Retourner les résultats sous un format structuré
        return {
            "status": plant_data.get("status", ""),
            "diag": plant_data.get("diag", ""),
            "solution": plant_data.get("solution", ""),
            "isPlant": plant_data.get("isPlant", 0)
        }, 200

    except openai.APIError as e:
        return {"error": "Erreur API OpenAI", "details": str(e)}, 500
    except Exception as e:
        return {"error": "Erreur interne", "details": str(e)}, 500
