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
                available_fields = {k: v for k, v in character.items() if v and v != []}
            else:
                error = "Aucun personnage trouvé."
        else:
            error = "Erreur lors de la requête vers l'API."

    return render_template("index.html", character=character, available=available_fields, error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
