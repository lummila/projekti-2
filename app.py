from flask import Flask, Response, request
from flask_cors import CORS
from game import Player
import json

app = Flask(__name__)
CORS(app)


@app.route("/register")  # type: ignore
def register():
    # Rekisteröityminen
    args = request.args

    username = str(args.get("username"))
    pin_code = str(args.get("password"))

    # Luodaan kirjautuvasta pelaajasta uusi instanssi
    pelaaja = Player()

    pelaaja.name = username.upper()

    login = pelaaja.login(username, pin_code)
    if login == -1:
        output = {"ERROR": "Login failed"}
        status_code = 200
    else:
        output = pelaaja.update(True)
        status_code = 200

    output_json = json.dumps(output)
    return Response(output_json, status_code, mimetype="application/json")


# @app.route("/action")  # type: ignore
# def action():
#     # Lentäminen ja työskentely
#     return


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
