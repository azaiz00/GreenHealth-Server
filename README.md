# GreenHealth-Server

- Analyse de la Santé des Plantes avec OpenAI 🤖

## Description

**GreenHealth-Server** est une API Flask qui analyse les images de plantes envoyées sous forme **Base64** (depuis Power Automate ou toute autre source).  
Elle utilise **OpenAI (GPT-4o)** pour identifier si la plante est en bonne santé, malade, ou si l'image ne contient pas de plante.  
Le résultat est retourné sous forme **HTML + JSON**, prêt à être utilisé dans Power Platform ( ou autre ).

---

## Structure du Projet

```
/GreenHealth-Server/
│── /templates/              <-  Dossier contenant les fichiers HTML
│   ├── error_not_plant.html   <- Si l'image n'est pas une plante
│   ├── healthy_plant.html     <- Si la plante est en bonne santé
│   ├── sick_plant.html        <- Si la plante est malade
│── /src                     <-  Dossier contenant les fichiers HTML
│   ├── ImageProcessing.py     <- Analyse de l'image avec OpenAI
│── .env.example               <- Exemple du fichier d'environnement
│── .gitignore                 <- Exclut les fichiers sensibles
│── app.py                     <- API Flask qui gère la requête
│── requirements.txt           <- Dépendances Python
│── README.md                  <- Documentation
```

---

## Installation et Configuration

### 1️⃣ **Cloner le projet**

```bash
git clone git@github.com:azaiz00/GreenHealth-Server.git
cd GreenHealth-Server

```

### 2️⃣ **Créer un environnement virtuel**

```bash
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate    # Windows
```

### 3️⃣ **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Configurer les variables d'environnement**

🔹 **Créer un fichier `.env`** à la racine du projet :

```bash
cp .env.example .env
```

🔹 **Ouvrir `.env`** et ajouter votre clé OpenAI :

```env
OPENAI_API_KEY="votre-clé-API-ici"
```

**Ne partagez jamais votre clé API !**

---

## Lancer l'API Flask

```bash
python app.py
```

L'API sera disponible sur **`http://127.0.0.1:5000/analyze`**

---

## **Utilisation avec Power Automate**

### **Envoyer une image encodée en Base64**

Power Automate doit envoyer une requête **POST** vers l'API Flask avec ce JSON :

```json
{
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAA..."
}
```

### **Réponse de l'API (Exemple)**

```json
{
  "HtmlResult": "<html>...</html>",
  "isPlant": 1
}
```

| **Champ**    | **Description**                                       |
| ------------ | ----------------------------------------------------- |
| `HtmlResult` | Contient le **code HTML** du diagnostic               |
| `isPlant`    | `1` = C'est une plante, `0` = Ce n'est pas une plante |

---
