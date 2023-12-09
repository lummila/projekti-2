from flask import Flask, Response, request
from flask_cors import CORS
from game import Player
import json

app = Flask(__name__)
CORS(app)


# Muuttuja pelaajaa varten. Sovellus tukee vain yhtä aktiivista pelaajaa tällä hetkellä.
# Funktiot käsittelevät pelaajaa global-avainsanalla, jotta data pysyy oliossa.
pelaaja = Player()


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

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Nollataan pelaajan tiedot ennen uutta kirjautumista sekaannuksen välttämiseksi.
    pelaaja = Player()
    # Login palauttaa True jos kirjautuminen onnistuu
    login = pelaaja.login(username, pin_code)
    if not login:
        output = {"ERROR": "Login failed"}
        status_code = 400
    else:
        output = {
            "name": pelaaja.name,
            "money": pelaaja.money,
            "location": pelaaja.location,
            "emissions": pelaaja.emissions,
            "possible_destinations": pelaaja.possible_locations(
                pelaaja.location, pelaaja.can_travel
            ),
            "hint": pelaaja.hint(),
            "round": pelaaja.round,
            "coincidence": "Nothing of note has happened.",
        }
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


@app.route("/register")  # type: ignore
def register():
    username, pin_code = stringify_credentials(
        request.args.get("username"), request.args.get("password")
    )

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Nollataan pelaajan tiedot ennen uutta kirjautumista sekaannuksen välttämiseksi.
    pelaaja = Player()
    # Register palauttaa True, jos rekisteröityminen onnistui
    register = pelaaja.register(username, pin_code)
    if not register:
        output = {"ERROR": "Register failed"}
        status_code = 400
    else:
        output = {
            "name": pelaaja.name,
            "money": pelaaja.money,
            "location": pelaaja.location,
            "emissions": pelaaja.emissions,
            "possible_destinations": pelaaja.possible_locations(
                pelaaja.location, pelaaja.can_travel
            ),
            "hint": pelaaja.hint(),
            "round": pelaaja.round,
            "coincidence": "Nothing of note has happened.",
        }
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


@app.route("/update")  # type: ignore
def update():
    flying = str(request.args.get("fly"))

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Onko pelaaja lentämässä paikasta toiseen?
    if flying == "yes":
        # update() pyöräyttää sattuman onnenpyörää eli lennetään
        output = json.dumps(pelaaja.update(True))
    else:
        # update() ei pyöräytä sattuman onnenpyörää eli työskennellään
        output = json.dumps(pelaaja.update(False))

    return Response(output, 200, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
