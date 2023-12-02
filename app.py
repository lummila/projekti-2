from flask import Flask, Response
from flask_cors import CORS
import game
import json

app = Flask(__name__)
CORS(app)


@app.route("/<name>/<pincode>")
def play(name, pincode):
    pelaaja = game.Player("")

    login = pelaaja.login(name, pincode)

    if login == -1:
        error_json = json.dumps({"ERROR": "Username not found, or PIN code was wrong."})
        return Response(response=error_json, status=400)

    update_json = json.dumps(pelaaja.update())

    return Response(response=update_json, status=200)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
