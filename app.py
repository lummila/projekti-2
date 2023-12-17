from flask import Flask, Response, request
from flask_cors import CORS
from game import Player
import json

app = Flask(__name__)
CORS(app)


# Muuttuja pelaajaa varten. Sovellus tukee vain yhtä aktiivista pelaajaa tällä hetkellä.
# Funktiot käsittelevät pelaajaa global-avainsanalla, jotta data pysyy oliossa.
pelaaja = Player()


# Kirjautuminen
# /login?username=_&password=_
@app.route("/login")
def login():
    # Käyttäjänimi ja PIN-koodi otetaan ehdoista
    username, pin_code = (
        str(request.args.get("username")),
        str(request.args.get("password")),
    )

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Nollataan pelaajan tiedot ennen uutta kirjautumista sekaannuksen välttämiseksi.
    pelaaja = Player()
    # Login palauttaa True jos kirjautuminen onnistuu
    login = pelaaja.login(username, pin_code)
    # Kirjautuminen epäonnistui
    if not login:
        output = {"ERROR": "No user information found. Please check you credentials."}
        status_code = 400
    # Kirjautuminen onnistui
    else:
        pelaaja.update()
        output = {"username": pelaaja.name, "password": pin_code}
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


# /register?username=_&password=_
@app.route("/register")
def register():
    username, pin_code = (
        str(request.args.get("username")),
        str(request.args.get("password")),
    )

    # Ilman globalia pelaaja on funktion sisäinen muuttuja johon ei pääse sen ulkopuolelta.
    global pelaaja

    # Nollataan pelaajan tiedot ennen uutta kirjautumista sekaannuksen välttämiseksi.
    pelaaja = Player()
    # Register palauttaa True, jos rekisteröityminen onnistui
    register = pelaaja.register(username, pin_code)

    if not register:
        output = {"ERROR": "Username already exists."}
    else:
        output = pelaaja.update()

    output_json = json.dumps(output)
    return Response(output_json, 200, mimetype="application/json")


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

    # Pelaaja yrittää lentää samaan maahan, missä on tällä hetkellä.
    if pelaaja.location == destination:
        # Pelaajan tiedot ovat samat kuin edellisellä kierroksella.
        output = pelaaja.update()
        status_code = 200
    else:
        # Kutsutaan fly()-metodi kohteeseen. Palauttaa booleanin.
        flight = pelaaja.fly(destination)
        # Pelaajalla ei ole rahaa tähän lentoon.
        if not flight:
            output = pelaaja.update()
            # Yliajetaan update()n sattumaominaisuus.
            output[
                "coincidence"
            ] = "You don't have enough money! Consider going to work."
            status_code = 200
        else:
            output = pelaaja.update()
            # Luodaan pelaajalle sattumateksti riippuen siitä, onko hän oikeassa paikassa.
            output["coincidence"] = pelaaja.coincidence(pelaaja.can_travel)
            status_code = 200
            # print(output["coincidence"])

    # HUOM JOS PELAAJAN SIJAINTI ON SAMA KUIN ROTAN VIIMEINEN = PELI ON VOITETTU!
    # print(pelaaja.location, pelaaja.rotta_destination_list[4])
    if pelaaja.location == pelaaja.rotta_destination_list[4]:
        # Pelaajan pisteet tallennetaan tietokantaan ja pisteet palautetaan
        final_score = pelaaja.game_over()

        # Viedään käyttäjälle kaikki tiedot ja uusi pistemäärä
        output = pelaaja.update()
        status_code = 200

        # Jos game_over() ei onnistu, ei ole pisteitä mitä näyttää
        if not final_score:
            output["final_score"] = "ERROR calculating points"
            status_code = 400
        else:
            # Käyttöliittymä tarkistaa, sisältääkö json final_scoren
            output["final_score"] = final_score

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


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
    # Palautetaan nykyisen käyttäjän huippupistemäärä
    if personal_score:
        scores = pelaaja.personal_high_score(pelaaja.name)

        # Jos omia huippupisteitä on olemassa
        if len(scores) > 0:
            # Palautetaan vain ensimmäinen rivi = suurin pistemäärä
            output[scores[0][0]] = scores[0][1]
        else:
            output = {"Empty": "No high scores available"}
    else:
        scores = pelaaja.high_score()
        # print(scores)

        # Jos huippupisteitä on olemassa
        if len(scores) > 0:
            for entry in scores:
                # Ensimmäinen indeksi on nimi, toinen on pistemäärä
                name = str(entry[0])
                points = entry[1]

                # Jos pelaajan nimi on jo listalla, mutta vähemmällä pistemäärällä, korvataan se isommalla pistemäärällä
                if name in output.keys() and output[name] < points:
                    output[name] = points
                # Jos nimeä ei ole pistelistalla, laitetaan se sille.
                elif name not in output.keys():
                    output[name] = points
        else:
            # Ei pisteitä saatavilla.
            output = {"Empty": "No high scores available"}

    # print(output)
    output_json = json.dumps(output)
    # print(output_json)

    return Response(output_json, 200, mimetype="application/json")


# Appin käynnistys
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
