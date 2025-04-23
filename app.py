# Traducción de campos al español
TRANSLATIONS = {
    "id": "ID",
    "name": "Nombre",
    "ki": "Ki",
    "max_ki": "Ki Máximo",
    "race": "Raza",
    "gender": "Género",
    "description": "Descripción",
    "image": "Imagen",
    "affiliation": "Afiliación",
    "originplanet": "Planeta de Origen",
    "transformations": "Transformaciones"
}

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    character = None
    error = None
    available_fields = {}

    if request.method == "POST":
        name = request.form["name"]
        url = f"https://dragonball-api.com/api/characters?name={name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                character = data[0]
                
                # Filtrer tous les champs non vides (None, "", [], {}, etc.)
                available_fields = {
                    k: v for k, v in character.items()
                    if v not in [None, "", [], {}, "null"]  # "null" en cas de string
                    and str(v).strip().lower() != "none"   # éviter 'None' en string
                    and str(k).lower() != "deletedat"      # champ inutile ou tech
                }
            else:
                error = "Aucun personnage trouvé."
        else:
            error = "Erreur lors de la requête vers l'API."

    return render_template("index.html", character=character, available=available_fields, error=error, translations=TRANSLATIONS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
