from flask import Flask, Response, request
from flask_cors import CORS
from game import Player
import json

app = Flask(__name__)
CORS(app)


# Tämä on koodieditoria varten luotu funktio, joka varmistaa että annetut ehdot ovat tekstiä.
# Muuten editori kohtelee näitä tuntemattomina tyyppeinä
def stringify_credentials(username, password):
    return str(username), str(password)


# Kirjautuminen
@app.route("/login")  # type: ignore
def login():
    # Käyttäjänimi ja PIN-koodi otetaan ehdoista
    username, pin_code = stringify_credentials(
        request.args.get("username"), request.args.get("password")
    )

    # Luodaan kirjautuvasta pelaajasta uusi instanssi
    pelaaja = Player()

    # Login palauttaa 
    login = pelaaja.login(username, pin_code)
    if not login:
        output = {"ERROR": "Login failed"}
        status_code = 400
    else:
        output = pelaaja.update(False)
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


@app.route("/register")  # type: ignore
def register():
    username, pin_code = stringify_credentials(
        request.args.get("username"), request.args.get("password")
    )

    # Luodaan pelaajan instanssi
    pelaaja = Player()

    register = pelaaja.register(username, pin_code)
    if not register:
        output = {"ERROR": "Register failed"}
        status_code = 400
    else:
        output = pelaaja.update(False)
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
