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
# /login?username=_&password=_
@app.route("/login")
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
        output = {"ERROR": "No user information found. Please check you credentials."}
        status_code = 400
    else:
        pelaaja.update()
        output = {"username": pelaaja.name, "password": pin_code}
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


# /register?username=_&password=_
@app.route("/register")
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
        output = {"ERROR": "Username already exists."}
        status_code = 400
    else:
        output = pelaaja.update()
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


# /update
@app.route("/update")
def update():
    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    output = pelaaja.update()
    output_json = json.dumps(output)

    return Response(output_json, 200, mimetype="application/json")


# /fly?dest=_
@app.route("/fly")
def fly():
    destination = str(request.args.get("dest"))

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    if pelaaja.location == destination:
        output = pelaaja.update()
    else:
        flight = pelaaja.fly(destination)
        if not flight:
            output = {"ERROR": "Not enough money"}
        else:
            output = pelaaja.update()
            output["coincidence"] = pelaaja.coincidence(pelaaja.can_travel)
            print(output["coincidence"])

    # HUOM JOS PELAAJAN SIJAINTI ON SAMA KUIN ROTAN VIIMEINEN = PELI ON VOITETTU!
    print(pelaaja.location, pelaaja.rotta_destination_list[4])
    if pelaaja.location == pelaaja.rotta_destination_list[4]:
        # Pelaajan pisteet tallennetaan tietokantaan ja pisteet palautetaan
        final_score = pelaaja.game_over()

        # Viedään käyttäjälle kaikki tiedot ja uusi pistemäärä
        output = pelaaja.update()
        # Käyttöliittymän tulee tarkistaa, sisältääkö json final_scoren
        output["final_score"] = final_score

    output_json = json.dumps(output)
    return Response(output_json, 200, mimetype="application/json")


# /work
@app.route("/work")
def work():
    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Pelaaja saa 175 € tililleen
    pelaaja.work()

    # Päivitetään pelaajan tiedot käyttöliittymään (False = ei sattumaa)
    output = json.dumps(pelaaja.update())

    return Response(output, 200, mimetype="application/json")


# /highscore?personal=_
@app.route("/highscore")
def high_score():
    # Omat jos personal=yes
    personal_score = True if request.args.get("personal") == "true" else False

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    output = {}
    if personal_score:
        scores = pelaaja.personal_high_score(pelaaja.name)

        # Jos omia huippupisteitä on olemassa
        if len(scores) > 0:
            for entry in scores:
                output[entry[0]] = entry[1]
        else:
            output = {"Empty": "No high scores available"}
    else:
        scores = pelaaja.high_score()

        # Jos huippupisteitä on olemassa
        if len(scores) > 0:
            for entry in scores:
                output[entry[0]] = entry[1]
        else:
            output = {"Empty": "No high scores available"}

    output_json = json.dumps(output)
    print(output_json)

    return Response(output_json, 200, mimetype="application/json")


@app.route("/reset")
def reset():
    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    name = pelaaja.name
    pelaaja = Player()
    pelaaja.name = name

    output = json.dumps({"Success": "Game reset"})

    return Response(output, 200, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
