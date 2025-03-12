# GreenHealth-Server

- Analyse de la Santé des Plantes avec OpenAI 🤖

## Description

**GreenHealth-Server** est une API Flask qui analyse les images de plantes envoyées sous forme **Base64** (depuis Power Automate ou toute autre source).  
Elle utilise **OpenAI (GPT-4o)** pour identifier si la plante est en bonne santé, malade, ou si l'image ne contient pas de plante.  
Le résultat est retourné sous deux formats :
- **HTML intégré dans un JSON** (pour un rendu direct dans PowerApps ou des applications web).
- **JSON structuré** (pour une intégration directe dans des pipelines de traitement de données ou d'autres applications).

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

L'API sera disponible aux adresses suivantes :
- **JSON + HTML :** `http://127.0.0.1:5000/analyze`
- **JSON structuré :** `http://127.0.0.1:5000/analyze_json_return`

---

## **Utilisation avec Power Automate**

### **Envoyer une image encodée en Base64**

Power Automate doit envoyer une requête **POST** vers l'API Flask avec ce JSON :

```json
{
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAA..."
}
```

### **Réponses de l'API**

#### **Option 1 : JSON avec HTML intégré (`/analyze`)**

```json
{
  "HtmlResult": "<html>...</html>",
  "isPlant": "1"
}
```

| **Champ**    | **Description**                                  |
|-------------|-----------------------------------------------|
| `HtmlResult` | Contient le **code HTML** du diagnostic     |
| `isPlant`    | `1` = C'est une plante, `0` = Ce n'est pas une plante |

#### **Option 2 : JSON structuré (`/analyze_json_return`)**

```json
{
  "status": "Bonne santé",
  "diag": "La plante est en bon état avec aucun problème visible.",
  "solution": "Maintenez un bon apport en lumière et en eau.",
  "isPlant": 1
}
```

| **Champ**    | **Description**                                    |
|-------------|--------------------------------------------------|
| `status`    | État de santé de la plante (`Bonne santé`, `Malade`, `Très malade`) |
| `diag`      | Explication détaillée de l'état de la plante   |
| `solution`  | Actions recommandées pour maintenir ou améliorer la santé de la plante |
| `isPlant`   | `1` = C'est une plante, `0` = Ce n'est pas une plante  |

---

