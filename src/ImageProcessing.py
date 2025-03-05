import openai
import json
import os
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
    """
    Analyse une image de plante avec GPT-4o et retourne un diagnostic structuré.
    """
    try:
        # Envoyer la requête à OpenAI pour obtenir le diagnostic
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Vous êtes un expert en botanique. Fournissez UNIQUEMENT un JSON structuré sous ce format : { 'status': 'good health' | 'sick' | 'very sick' | '', 'diag': 'Explication...', 'solution': 'Solution...', 'isPlant': 1 ou 0 }. PAS DE TEXTE SUPPLÉMENTAIRE."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Voici une photo d'une plante. Fournissez un diagnostic structuré au format JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]},
            ],
            temperature=0.3,
            max_tokens=300
        )

        # Vérifier si la réponse OpenAI contient des choix
        if not response.choices:
            return {"error": "Erreur API OpenAI", "details": "Réponse vide d'OpenAI"}, 500

        # Convertir la réponse en JSON
        try:
            plant_data = json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            return {"error": "Erreur de parsing de la réponse OpenAI", "details": str(e)}, 500

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
